# Lab.AWS.API-Gateway

**Creating a serverless API using AWS SAM, OpenAPI 3.0 and Lambda Powertools - writing clean Code with Python**

"Work smart, not hard" means using the best tools for the job. Developers also say "be lazy, write less code".
Serverless technology does not only allow to outsource server and network maintenance and focus on the application, it also allows to focus on cleaner code.

This article brings together several tweeks of the serverless world of the last years:

* **AWS Serverless Application Model** (SAM) - [An open-source framework for building serverless applications on AWS](https://aws.amazon.com/serverless/sam/)
* **OpenAPI** 3.0 - [An open-source API definition language supported by AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-swagger-extensions.html)
* **Powertools for AWS Lambda** - [A developer toolkit to implement Serverless best practices and increase developer velocity](https://docs.powertools.aws.dev/lambda/python/latest/)

It puts also a strong focus on clean code:

* **MVC pattern** - https://python.plainenglish.io/model-view-controller-mvc-pattern-in-python-a-beginners-guide-b0d9855068eb
* **Repository pattern** - https://medium.com/@pererikbergman/repository-design-pattern-e28c0f3e4a30
* **Validators**
* **Router**

## High level architecture

A basic API Gateway setup with Lambda Powertools consists of:

* **The REST API** (AWS API Gateway) - Exposes endpoints and receives requests
* **The API handler** (AWS Lambda) - Processes the requests
* **A table** (AWS DynamoDB) - Stores the data

<!-- Edit: https://mermaid.live/ -->
```mermaid
flowchart LR

API("`
   AWS API Gateway
   ConcertsAPI
`") -->|invoke| Handler

Handler("`
   AWS Lambda
   concerts_api_handler
`") -->|query| Table
Handler -->|response| API

Table[("`
   AWS DynamoDB
   ConcertsTable
`")] -->|Concerts| Handler
```

## Implementation details

### Entrypoint: The API Gateway

The OpenAPI 3.0 specification allows, to define an API in an interoperable opensource format and deploy an API Gateway based on it. Furthermore it can be used to generate a Swagger documentation.

For each endpoint, a "path" needs to be defined:

```yaml
# src/api/concerts.yaml

paths:
  /concerts:
    get:
      description: Returns a list of concerts
      parameters:
        - in: query
          name: artist
          schema:
            type: string
          description: Artist to filter the concerts
      responses:
        200:
          description: Successfully retrieved concerts
```

For the integration with Lambda, AWS provides a proxy integration:

```yaml
      x-amazon-apigateway-integration:
        httpMethod: POST
        payloadFormatVersion: "2.0"
        timeoutInMillis: 10000
        passthroughBehavior: "when_no_match"
        type: aws_proxy
        uri:
          Fn::Sub: "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ApiHandlerFunction.Arn}/invocations"
```

Important detail: The payloadFormatVersion must match the API Gateway version. Otherwise the event format will not match and the API will fail with errors like "field httpProtocol can not be found.", because the event structures are not backward-compatible.

The OpenAPI specification can then be linked into the SAM template. Embedding the specification using "AWS::Include" allows to use references, like "${ApiHandlerFunction.Arn}":

```yaml
# src/template.yml

  ConcertsApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: !Ref env
      DefinitionBody:
        "Fn::Transform":
          Name: "AWS::Include"
          Parameters:
            Location: "./api/concerts.yaml"
```

For details see [concerts.yaml](./src/api/concerts.yaml) and [template.yml](./src/template.yml).


### Request handler: The API-handler Lambda function

To build a single API handler Lambda function, with shared components like models or repositories, [Powertools Event Handler for REST API](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/) provides a router, called resolver.

Using this router as an entry point for the Lambda function, a MVC like, well structured Lambda function can be implemented, containing the following components:

* **Request router** (Powertools APIGatewayHttpResolver): [index.py](./src/lambda/concerts_api_handler/index.py) - Is responsible to route the requests to the corresponding controller action, based on the path information from API Gateway, which it get's embedded in the event.
* **Controller**: [controller/concerts_controller.py](./src/lambda/concerts_api_handler/src/controller/concerts_controller.py) - Is responsible to process the request parameters, validate them and invoke the repository, to get or create Concerts.
* **Model**: [model/concert.py](./src/lambda/concerts_api_handler/src/model/concert.py) - Represents a Concert object.
* **Repository**: [repository/concerts_repository.py](./src/lambda/concerts_api_handler/src/repository/concerts_repository.py) - Is responsible to persist and retrieve concert records to and from the DynamoDB database.

Furthermore Powertools offers nice utilities for:

* **Logging** - [Powertools logger](https://docs.powertools.aws.dev/lambda/python/latest/core/logger/)
* **Tracing** - [Powertools tracer](https://docs.powertools.aws.dev/lambda/python/latest/core/tracer/)

<!-- Edit: https://mermaid.live/ -->
```mermaid
classDiagram

class APIGatewayHttpResolver {
   get()
   put()
   resolve()
}

router --|> APIGatewayHttpResolver
router: get_concerts()
router: put_concert()
router --> ConcertController: resolve route

class ConcertController {
   get_concerts_action()
   put_concert_action()
}
ConcertController --> ConcertRepository: Find / Create concert(s)
ConcertController --> concert_validator: Validate event

concert_validator: validate_get_concerts_event()
concert_validator: validate_put_concert_event()

class Concert {
   string artist
   string concert
   int ticket_sales
   string created_date
}

class ConcertRepository {
   find_concert_by_artist()
   create_concert()
}
```

SAM's "Serverless::Function" resource simplifies the deployment of such a Lambda function:

```yml
# src/template.yml

  ApiHandlerFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.lambda_handler
      Runtime: python3.9
      CodeUri: "./lambda/concerts_api_handler/src"
      Layers:
        - !Sub "arn:aws:lambda:${AWS::Region}:017000801446:layer:AWSLambdaPowertoolsPythonV2-Arm64:43"
      Tracing: Active
      Timeout: 10
      Architectures:
        - arm64
      Environment:
        Variables:
          TABLE_NAME: !Ref ConcertsTable
          LOG_LEVEL: !If [IsEnvProd, "WARNING", "INFO"]
          POWERTOOLS_LOGGER_LOG_EVENT: !If [IsEnvProd, false, true]
          POWERTOOLS_SERVICE_NAME: concerts_api_handler
      Policies:
        - AWSLambdaExecute
        - Version: "2012-10-17"
          Statement:
            - Effect: Allow
              Action:
                - dynamodb:Query
                - dynamodb:PutItem
              Resource: !GetAtt ConcertsTable.Arn
```

### Persistence: The DynamoDB table

To store concerts, a simple DynamoDB table is used:

```yaml
# src/template.yml

  ConcertsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      TableName: !Sub "concerts-${env}"
      AttributeDefinitions:
        - AttributeName: artist
          AttributeType: S
        - AttributeName: concert
          AttributeType: S
      KeySchema:
        - AttributeName: artist
          KeyType: HASH
        - AttributeName: concert
          KeyType: RANGE
```

Concerts are stored as simple records like:

```json
{
    "artist": "Madonna",
    "concert": "This is Madonna 2023",
    "ticket_sales": 5000000,
    "created_date": "2023-09-08T14:47:29.915661"
}
```

---

## Development

### Dependencies

1. Install latest AWS CLI https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html
2. Install AWS SAM CLI https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
3. Install Python 3.9


### Recommended Visual Studio Code plugins

* https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml
* https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml
* https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one


## Deployment

For instructions regarding SAM, see https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli.html.

```sh
cd src
```

```sh
# Build & deploy
sam build
sam deploy --config-env dev
```

```sh
# Develop interactively
sam sync --stack-name concerts-api-dev --watch
```

```sh
# Stack outputs
sam list stack-outputs --stack-name concerts-api-dev
```

```sh
# Delete stack
sam delete --config-env dev
# or
aws cloudformation delete-stack --stack-name concerts-api-dev
# To remove all SAM resources completely, als the stack aws-sam-cli-managed-default needs to be deleted
aws cloudformation delete-stack --stack-name aws-sam-cli-managed-default
```

## Try it out

### Create a concert

```sh
# Replace API_ID by the actual ID
curl -X PUT --location 'https://{API_ID}.execute-api.eu-central-1.amazonaws.com/dev/concerts' \
    -H 'Content-Type: application/json' \
    -d '{"artist":"Madonna","concert":"This is Madonna 2023","ticket_sales": 5000000 }'
```

### List concerts

Open [https://{API_ID}.execute-api.eu-central-1.amazonaws.com/dev/concerts?artist=Madonna](https://{API_ID}.execute-api.eu-central-1.amazonaws.com/dev/concerts?artist=Madonna) in your browser (replace API_ID by the actual ID)


## Additional Resources

* Python doc comments with Sphinx: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#python-signatures

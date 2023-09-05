# Lab.AWS.API-Gateway

A basic API Gateway example with Lambda Powertools router:

* OpenAPI 3 template
* [Lambda Powertools for Python](https://docs.powertools.aws.dev/lambda/python/latest/core/event_handler/api_gateway/)
* Modular handler Lambda:
    * Request router: [index.py](./src/lambda/concerts_api_handler/index.py)
    * Controller: [controller/concerts_controller.py](./src/lambda/concerts_api_handler/controller/concerts_controller.py)
    * Model: [model/concert.py](./src/lambda/concerts_api_handler/model/concert.py)
    * Repository: [repository/concerts_repository.py](./src/lambda/concerts_api_handler/repository/concerts_repository.py)
* Logging: Powertools logger
* Tracing: Powertools tracer


## Development

### Dependencies

1. Install latest AWS CLI https://docs.aws.amazon.com/cli/latest/userguide/getting-started-version.html
2. Install AWS SAM CLI https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
3. Install Python 3.9


### Recommended Visual Studio Code plugins

* https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml


## Deployment

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli.html

```sh
cd src
```

```sh
# Build & deploy
sam build
sam deploy --config-env dev
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
```

## Resources

* Python doc comments with Sphinx: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#python-signatures
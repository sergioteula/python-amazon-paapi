# Migration guide from 4.x to 5.x

This guide explains how to proceed with the migration from version 4.x to version 5.x of your current code.
If you are still using the old version, it is highly recommended to update, since you wont get any future
updates nor new features.

## Changelog summary

- Updated custom exceptions names.

## How to upgrade?

Upgrading to the last version of this module is as easy as running this pip command:

    pip install python-amazon-paapi --upgrade

## What should I change in my current code?

### Exceptions

Exceptions names have changed, removing the `Exception` part of the name or replacing it
with `Error`. They should be adjusted as bellow:

```python
AmazonException                 ->  AmazonError
AsinNotFoundException           ->  AsinNotFound
AssociateValidationException    ->  AssociateValidationError
InvalidArgumentException        ->  InvalidArgument
InvalidPartnerTagException      ->  InvalidPartnerTag
ItemsNotFoundException          ->  ItemsNotFound
MalformedRequestException       ->  MalformedRequest
ApiRequestException             ->  RequestError
TooManyRequestsException        ->  TooManyRequests
```

### I need more help

You can always ask for help in our [Telegram group](https://t.me/PythonAmazonPAAPI) or raise an issue on
[Github](https://github.com/sergioteula/python-amazon-paapi/issues) for help. If you find that this
guide could be improved somehow, feel free to send a pull request with your changes.

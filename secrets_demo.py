""" example of gettingand setting secrets using AWS Secret Manager """

import os
import random
import string
import boto3
from botocore.exceptions import ClientError


def get_random_string():
    """ generates a random string """

    random_string = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(32)]
    )
    return random_string


def get_client():
    """ get boto client to use here """

    endpoint_url = "https://secretsmanager.eu-west-1.amazonaws.com"
    region_name = "eu-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )

    return client


def set_secret(secret_name, secret_value):
    """ stores secret in AWS Secret Manager """

    client = get_client()

    print('--------------------')
    print('setting secret')
    print('secret name: {}'.format(secret_name))
    print('secret value: {}'.format(secret_value))

    client.put_secret_value(
        SecretId=secret_name,
        SecretString=secret_value
    )


def get_secret(secret_name):
    """ calls AWS Secret Manager to get secret """
    secret = "{}"
    client = get_client()

    print('--------------------')
    print('retrieving secret')

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as exception:
        if exception.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif exception.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", exception)
        elif exception.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", exception)
    else:
        # Decrypted secret using the associated KMS CMK
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = get_secret_value_response['SecretBinary']

    return secret


def main():
    """ main function """
    secret_name = "test1"
    random_string = get_random_string()

    set_secret(secret_name, random_string)

    retrieved_secret_value = get_secret(secret_name)
    if not retrieved_secret_value:
        print("Secret Empty")
        os._exit(1)

    print("retrieved secret: {}".format(retrieved_secret_value))


if __name__ == "__main__":
    main()

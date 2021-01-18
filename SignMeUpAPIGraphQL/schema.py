import graphene
import graphql_jwt

import api
from api import retrieve_schema,create_schema,delete_schema,update_schema,file_schema


class Query(
    api.retrieve_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(api.create_schema.Mutation,
               api.delete_schema.Mutation,
               api.update_schema.Mutation,
               api.file_schema.Mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

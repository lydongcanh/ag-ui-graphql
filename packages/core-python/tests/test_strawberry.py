import unittest

try:
    import strawberry  # noqa: F401
except ImportError:  # pragma: no cover - optional extra
    strawberry = None  # type: ignore[assignment]

from ag_ui_graphql.events import event_to_graphql_event


@unittest.skipIf(strawberry is None, "strawberry-graphql not installed")
class StrawberryTypesTest(unittest.TestCase):
    def test_projects_domain_event_into_graphql_type(self) -> None:
        from ag_ui_graphql.integrations.strawberry import GraphQLAgentEventType

        domain_event = event_to_graphql_event(
            {
                "type": "TEXT_MESSAGE_CONTENT",
                "messageId": "m1",
                "delta": "hello",
            }
        )

        gql_event = GraphQLAgentEventType.from_domain(domain_event)

        self.assertEqual(gql_event.type, "TEXT_MESSAGE_CONTENT")
        self.assertEqual(gql_event.message_id, "m1")
        self.assertEqual(gql_event.text_delta, "hello")
        self.assertEqual(gql_event.payload["delta"], "hello")
        self.assertEqual(gql_event.hitl_requirements, [])

    def test_subscription_field_emits_envelope(self) -> None:
        import strawberry as sb
        from typing import AsyncIterator

        from ag_ui_graphql.integrations.strawberry import GraphQLAgentEventType

        @sb.type
        class Query:
            @sb.field
            def health(self) -> str:
                return "ok"

        @sb.type
        class Subscription:
            @sb.subscription
            async def run_agent(self) -> AsyncIterator[GraphQLAgentEventType]:
                yield GraphQLAgentEventType.from_domain(
                    event_to_graphql_event(
                        {"type": "RUN_STARTED", "threadId": "t", "runId": "r"}
                    )
                )

        schema = sb.Schema(query=Query, subscription=Subscription)
        sdl = str(schema)

        self.assertIn("type GraphQLAgentEvent", sdl)
        self.assertIn("runAgent: GraphQLAgentEvent!", sdl)


if __name__ == "__main__":
    unittest.main()

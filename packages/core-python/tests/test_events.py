import unittest

from ag_ui_graphql.events import event_to_graphql_event


class EventsTest(unittest.TestCase):
    def test_projects_ag_ui_event_to_graphql_envelope(self) -> None:
        event = event_to_graphql_event(
            {
                "type": "TEXT_MESSAGE_CONTENT",
                "messageId": "m1",
                "delta": "hello",
            }
        )

        self.assertEqual(event.type, "TEXT_MESSAGE_CONTENT")
        self.assertEqual(event.message_id, "m1")
        self.assertEqual(event.text_delta, "hello")
        self.assertEqual(event.to_graphql()["messageId"], "m1")


if __name__ == "__main__":
    unittest.main()

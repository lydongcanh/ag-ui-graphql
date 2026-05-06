import {
  AbstractAgent,
  type AgentConfig,
  type BaseEvent,
  type RunAgentInput,
} from "@ag-ui/client";
import { Observable } from "rxjs";
import { unwrapGraphQLAgentEvent } from "./events";
import type { GraphQLRunExecutor } from "./types";

export interface GraphQLAgentConfig extends AgentConfig {
  execute: GraphQLRunExecutor;
}

export class GraphQLAgent extends AbstractAgent {
  private readonly execute: GraphQLRunExecutor;
  private readonly config: GraphQLAgentConfig;
  private abortController = new AbortController();

  constructor(config: GraphQLAgentConfig) {
    const { execute: _execute, ...agentConfig } = config;
    super(agentConfig);
    this.execute = config.execute;
    this.config = config;
  }

  run(input: RunAgentInput): Observable<BaseEvent> {
    this.abortController = new AbortController();

    return new Observable<BaseEvent>((subscriber) => {
      let active = true;

      const pump = async () => {
        try {
          const stream = await this.execute(input, {
            signal: this.abortController.signal,
          });

          for await (const event of stream) {
            if (!active || this.abortController.signal.aborted) {
              break;
            }

            subscriber.next(unwrapGraphQLAgentEvent(event));
          }

          if (active) {
            subscriber.complete();
          }
        } catch (error) {
          if (active) {
            subscriber.error(error);
          }
        }
      };

      void pump();

      return () => {
        active = false;
        this.abortController.abort();
      };
    });
  }

  abortRun(): void {
    this.abortController.abort();
  }

  clone(): GraphQLAgent {
    return new GraphQLAgent({
      ...this.config,
      agentId: this.agentId,
      description: this.description,
      threadId: this.threadId,
      initialMessages: this.messages,
      initialState: this.state,
    });
  }
}

import { z } from "zod"

/**Base schema for all 33GOD events. Provides common fields for event routing, tracing, and correlation. All domain events extend this base. Domain-specific fields (e.g., meeting_id for TheBoard) are added via domain extensions.*/
export const BaseEvent = z.object({ 
/**Unique identifier for this event instance*/
"event_id": z.any().describe("Unique identifier for this event instance"), 
/**Event discriminator for routing (e.g., 'agent.message.received'). Used by Bloodbank for topic-based routing.*/
"event_type": z.string().regex(new RegExp("^[a-z0-9]+\\.[a-z0-9._]+$")).describe("Event discriminator for routing (e.g., 'agent.message.received'). Used by Bloodbank for topic-based routing."), 
/**ISO 8601 UTC timestamp when event was emitted*/
"timestamp": z.any().describe("ISO 8601 UTC timestamp when event was emitted"), 
/**Schema version for this event type*/
"version": z.any().describe("Schema version for this event type").default("1.0.0"), 
/**UUID for tracing related events through the system. All events in a causal chain share the same correlation_id.*/
"correlation_id": z.any().describe("UUID for tracing related events through the system. All events in a causal chain share the same correlation_id."), 
/**ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.*/
"causation_id": z.any().describe("ID of the event or command that directly caused this event. Together with correlation_id, forms a directed acyclic graph of causation. Optional for root events.").optional(), 
/**Metadata about the source that emitted this event*/
"source": z.object({ 
/**Hostname of the emitting machine*/
"host": z.string().describe("Hostname of the emitting machine"), 
/**Application or service name (e.g., 'bloodbank', 'holocene', 'cack')*/
"app": z.string().describe("Application or service name (e.g., 'bloodbank', 'holocene', 'cack')"), 
/**What triggered this event*/
"trigger_type": z.enum(["cli","api","scheduled","event","webhook"]).describe("What triggered this event"), 
/**User or agent ID if applicable*/
"user_id": z.string().describe("User or agent ID if applicable").optional() }).describe("Metadata about the source that emitted this event") }).describe("Base schema for all 33GOD events. Provides common fields for event routing, tracing, and correlation. All domain events extend this base. Domain-specific fields (e.g., meeting_id for TheBoard) are added via domain extensions.")
export type BaseEvent = z.infer<typeof BaseEvent>

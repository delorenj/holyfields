import { z } from "zod"

/**Emitted when a message is posted in a brainstorming conversation*/
export const messagePostedEventSchema = z.object({ "event_type": z.literal("conversation.message.posted"), "timestamp": z.any(), "conversation_id": z.any(), "message_id": z.any(), 
/**ID of the author (user or agent)*/
"author_id": z.string().describe("ID of the author (user or agent)"), 
/**The message content*/
"content": z.string().describe("The message content"), 
/**ID of the message this is replying to*/
"reply_to_id": z.any().describe("ID of the message this is replying to").optional() }).describe("Emitted when a message is posted in a brainstorming conversation")
export type MessagePostedEvent = z.infer<typeof messagePostedEventSchema>

import { z } from "zod"

/**Emitted when a message is posted in a conversation*/
export const MessagePostedEventSchema = z.object({ 
/**Event type discriminator*/
"event_type": z.literal("conversation.message.posted").describe("Event type discriminator"), "payload": z.object({ 
/**UUID of the conversation*/
"conversation_id": z.any().describe("UUID of the conversation"), 
/**UUID of this message*/
"message_id": z.any().describe("UUID of this message"), 
/**ID of the author (user or agent)*/
"author_id": z.string().describe("ID of the author (user or agent)"), 
/**The message content*/
"content": z.string().min(1).describe("The message content"), 
/**ID of the message this is replying to*/
"reply_to_id": z.union([z.any(), z.null()]).describe("ID of the message this is replying to").optional() }) }).and(z.any()).describe("Emitted when a message is posted in a conversation")
export type MessagePostedEvent = z.infer<typeof MessagePostedEventSchema>

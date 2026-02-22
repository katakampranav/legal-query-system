import { httpPost } from "@/lib/http-client";
import type { AskRequest, AskResponse, ChatMode } from "../types/chat-types";

const ASK_ENDPOINT = "/api/v1/ask";

export async function sendMessage(
  question: string,
  mode: ChatMode
): Promise<string> {
  const payload: AskRequest = { question, mode };
  const response = await httpPost<AskRequest, AskResponse>(
    ASK_ENDPOINT,
    payload
  );
  return response.answer;
}

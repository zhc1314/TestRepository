import request from './request'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  user_id: string
  message: string
  history?: ChatMessage[]
}

export interface ChatResponse {
  message: string
  timestamp: string
}

/**
 * 发送聊天消息
 */
export const sendChatMessage = (data: ChatRequest): Promise<ChatResponse> => {
  return request({
    url: '/chat/',
    method: 'POST',
    data
  })
}

/**
 * 获取聊天历史
 */
export const getChatHistory = (userId: string) => {
  return request({
    url: `/chat/history/${userId}`,
    method: 'GET'
  })
}
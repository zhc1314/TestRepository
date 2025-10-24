import request from './request'

export interface UserProfile {
  id?: number
  user_id: string
  nickname?: string
  target_university?: string
  target_major?: string
  is_cross_major?: boolean
  major_subjects?: string[]
  target_total_score?: number
  target_politics_score?: number
  target_english_score?: number
  target_math_score?: number
  target_major_score?: number
  study_start_date?: string
  exam_date?: string
  weekday_study_hours?: number
  weekend_study_hours?: number
  remaining_days?: number
  politics_level?: string
  english_level?: string
  math_level?: string
  major_knowledge_score?: number
  major_knowledge_detail?: Record<string, any>
  study_time_preference?: string
  study_method_preference?: string
  weak_subject_priority?: string[]
  other_preferences?: string
  created_at?: string
  updated_at?: string
}

/**
 * 创建用户画像
 */
export const createUserProfile = (data: UserProfile) => {
  return request({
    url: '/user-profile/',
    method: 'POST',
    data
  })
}

/**
 * 获取用户画像
 */
export const getUserProfile = (userId: string) => {
  return request({
    url: `/user-profile/${userId}`,
    method: 'GET'
  })
}

/**
 * 更新用户画像
 */
export const updateUserProfile = (userId: string, data: Partial<UserProfile>) => {
  return request({
    url: `/user-profile/${userId}`,
    method: 'PUT',
    data
  })
}

/**
 * 删除用户画像
 */
export const deleteUserProfile = (userId: string) => {
  return request({
    url: `/user-profile/${userId}`,
    method: 'DELETE'
  })
}
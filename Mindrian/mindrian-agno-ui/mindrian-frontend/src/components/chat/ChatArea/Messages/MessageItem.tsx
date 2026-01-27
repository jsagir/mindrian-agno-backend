import Icon from '@/components/ui/icon'
import MarkdownRenderer from '@/components/ui/typography/MarkdownRenderer'
import { useStore } from '@/store'
import type { ChatMessage } from '@/types/os'
import Videos from './Multimedia/Videos'
import Images from './Multimedia/Images'
import Audios from './Multimedia/Audios'
import { memo } from 'react'
import AgentThinkingLoader from './AgentThinkingLoader'
import ReasoningBlock from './ReasoningBlock'
import ToolCallCard from './ToolCallCard'
import ReferencesBlock from './ReferencesBlock'

interface MessageProps {
  message: ChatMessage
}

const AgentMessage = ({ message }: MessageProps) => {
  const { streamingErrorMessage, showReasoning, showToolCalls, showReferences } = useStore()

  // Check if we have reasoning, tool calls, or references
  const hasReasoning = message.extra_data?.reasoning_steps && message.extra_data.reasoning_steps.length > 0
  const hasToolCalls = message.tool_calls && message.tool_calls.length > 0
  const hasReferences = message.extra_data?.references && message.extra_data.references.length > 0

  let messageContent
  if (message.streamingError) {
    messageContent = (
      <p className="text-destructive">
        Oops! Something went wrong while streaming.{' '}
        {streamingErrorMessage ? (
          <>{streamingErrorMessage}</>
        ) : (
          'Please try refreshing the page or try again later.'
        )}
      </p>
    )
  } else if (message.content) {
    messageContent = (
      <div className="flex w-full flex-col">
        {/* Reasoning Block - Collapsible thinking */}
        {showReasoning && hasReasoning && (
          <ReasoningBlock
            reasoning={message.extra_data!.reasoning_steps!}
            isStreaming={false}
          />
        )}

        {/* Tool Calls Block - Show executed tools */}
        {showToolCalls && hasToolCalls && (
          <ToolCallCard
            toolCalls={message.tool_calls!}
            isStreaming={false}
          />
        )}

        {/* Main Content */}
        <div className="flex w-full flex-col gap-4">
          <MarkdownRenderer>{message.content}</MarkdownRenderer>
          {message.videos && message.videos.length > 0 && (
            <Videos videos={message.videos} />
          )}
          {message.images && message.images.length > 0 && (
            <Images images={message.images} />
          )}
          {message.audio && message.audio.length > 0 && (
            <Audios audio={message.audio} />
          )}
        </div>

        {/* References Block - Citations */}
        {showReferences && hasReferences && (
          <ReferencesBlock references={message.extra_data!.references!} />
        )}
      </div>
    )
  } else if (message.response_audio) {
    if (!message.response_audio.transcript) {
      messageContent = (
        <div className="mt-2 flex items-start">
          <AgentThinkingLoader />
        </div>
      )
    } else {
      messageContent = (
        <div className="flex w-full flex-col gap-4">
          <MarkdownRenderer>
            {message.response_audio.transcript}
          </MarkdownRenderer>
          {message.response_audio.content && message.response_audio && (
            <Audios audio={[message.response_audio]} />
          )}
        </div>
      )
    }
  } else {
    // Streaming state - show reasoning/tools as they come in
    messageContent = (
      <div className="flex w-full flex-col">
        {/* Show reasoning while streaming */}
        {showReasoning && hasReasoning && (
          <ReasoningBlock
            reasoning={message.extra_data!.reasoning_steps!}
            isStreaming={true}
          />
        )}

        {/* Show tool calls while streaming */}
        {showToolCalls && hasToolCalls && (
          <ToolCallCard
            toolCalls={message.tool_calls!}
            isStreaming={true}
          />
        )}

        {/* Loading indicator if no reasoning/tools */}
        {!hasReasoning && !hasToolCalls && (
          <div className="mt-2">
            <AgentThinkingLoader />
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="flex flex-row items-start gap-4 font-geist">
      <div className="flex-shrink-0">
        <Icon type="agent" size="sm" />
      </div>
      {messageContent}
    </div>
  )
}

const UserMessage = memo(({ message }: MessageProps) => {
  return (
    <div className="flex items-start gap-4 pt-4 text-start max-md:break-words">
      <div className="flex-shrink-0">
        <Icon type="user" size="sm" />
      </div>
      <div className="text-md rounded-lg font-geist text-secondary">
        {message.content}
      </div>
    </div>
  )
})

AgentMessage.displayName = 'AgentMessage'
UserMessage.displayName = 'UserMessage'
export { AgentMessage, UserMessage }

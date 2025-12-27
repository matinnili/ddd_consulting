import events
import handlers

handler_dictionary = {
    events.InterviewCreateMessage: handlers.interview_creation_handler,
    events.InterviewCompleteMessage: handlers.interview_completion_handler,
}
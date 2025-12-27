import handler_dictionary
import events

def message_bus(event):

    queue=[event]
    while queue:
        event=queue.pop(0)
        handler=handler_dictionary[type(event)]
        handler(event)
        queue.extend(event.get_related_events())
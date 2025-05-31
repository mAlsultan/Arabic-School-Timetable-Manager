import random

grades = ['Grade 6', 'Grade 7', 'Grade 8']

subjects = ['Math', 'Science', 'English', 'History', 'Geography', 'ICT', 'Health', 'Art']

teachers = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']

# Updated qualified dictionary with more teachers for Grade 7 and Grade 8
qualified = {
    'T1': [('Grade 6', 'Math'), ('Grade 6', 'ICT'), ('Grade 7', 'Math'), ('Grade 7', 'ICT')],
    'T2': [('Grade 6', 'Science'), ('Grade 6', 'Health'), ('Grade 7', 'Science')],
    'T3': [('Grade 6', 'English'), ('Grade 7', 'English'), ('Grade 8', 'English')],
    'T4': [('Grade 6', 'History'), ('Grade 7', 'History')],
    'T5': [('Grade 6', 'Geography'), ('Grade 7', 'Geography'), ('Grade 8', 'Geography')],
    'T6': [('Grade 6', 'Art'), ('Grade 7', 'Art'), ('Grade 8', 'Art')],
    'T7': [('Grade 6', 'ICT'), ('Grade 7', 'ICT')],
    'T8': [('Grade 6', 'Health'), ('Grade 6', 'Math'), ('Grade 7', 'Health'), ('Grade 7', 'Math'), ('Grade 8', 'Math')],
    'T9': [('Grade 7', 'Math'), ('Grade 7', 'Science'), ('Grade 8', 'Math')],
    'T10': [('Grade 7', 'English'), ('Grade 8', 'English')],
    'T11': [('Grade 8', 'History'), ('Grade 8', 'Geography')],
    'T12': [('Grade 8', 'ICT'), ('Grade 8', 'Art')]
}

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
slots_per_day = 8



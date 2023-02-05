import sqlite3
import sys

connection = sqlite3.connect('todolist.db')
cursor = connection.cursor()

try:
    cursor.execute('CREATE TABLE tasks (task TEXT, timeframe TEXT, notes TEXT)')
except Exception:
    pass

def task_is_unique(new_task):
    rows = cursor.execute('SELECT * FROM tasks').fetchall()

    for task in rows:
        if task[0].lower() == new_task.lower():
            return False
    return True

def add_task():
    new_task = input('Task: ')

    if task_is_unique(str(new_task)):
        timeframe = input('Timeframe: ')
        notes = input('Notes: ')

        if new_task != '' and timeframe != '' and notes != '':
            cursor.execute(f"INSERT INTO tasks VALUES ('{new_task}','{timeframe}','{notes}')")
            connection.commit()
            print(new_task.capitalize() + ' has been added to the to do list.')
        else:
            print('Looks like something was left blank, please try again.')
            add_task()
    else:
        print('This task already exists please try adding something else')

def edit_task():
    edit_task = input('Which task would you like to update? ')
    update = input('What part do you want to update: task, timeframe, or notes? ')
    update_to_do = input('What do you want to change it to? ')

    try:
        cursor.execute(f'UPDATE tasks SET {update} = ? WHERE task = ?', (update_to_do, edit_task,))
        connection.commit()
        print(f'Updated {update} to {update_to_do}')
    except Exception:
        print('Update failed, try again')

def get_task():
    target = input('Which task do you want info on? ')
    info = cursor.execute('SELECT task, timeframe, notes FROM tasks WHERE task = ?', (target,)).fetchall()

    req_task = info[0][0]
    req_time = info[0][1]
    req_note = info[0][2]

    print(f' {req_task.capitalize()}\n -------\n {req_time}\n {req_note}\n -------')

def complete_task():
    target = input('Which task do you want to complete? ')
    if target != '':
        cursor.execute('DELETE FROM tasks WHERE task = ?', (target,))
        connection.commit()
        print('Task Completed!')
    else:
        print('Task not found')
    
def display_tasks():
    data = cursor.execute('SELECT * FROM tasks').fetchall()

    print('Tasks:')
    for task in data:
        print(task[0])

def exit_app():
    cursor.close()
    connection.close()
    sys.exit()

def selection():
    options = int(input('''

    Type 0 to display all tasks
    Type 1 to add a task
    Type 2 to edit a task
    Type 3 to comeplete a task
    Type 4 to get info on a task
    Type 5 to exit to do list

    > '''))
    if options == 0:
        display_tasks()
    elif options == 1:
        add_task()
    elif options == 2:
        edit_task()
    elif options == 3:
        complete_task()
    elif options == 4:
        get_task()
    elif options == 5:
        exit_app()

while True:
    selection()
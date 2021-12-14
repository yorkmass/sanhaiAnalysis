# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm');
    print(2//3);
    while True:
        try:
            t=int(input(''))
            if t==0:
                break
            tt=0
            while t>1:
                tt+=(t//3)
                t=(t//3)+(t%3)
                if t==2:
                    tt+=1
            print(tt)
        except:
            break

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

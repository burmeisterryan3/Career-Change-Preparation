while True:
    try:
        x = int(input('Enter the first number: '))
        y = int(input('Enter the second number: '))
        value = x / y
        print('x / y is', value)
    except ValueError:
        print('Invalid number. Please try again.')
    except ZeroDivisionError:
        print('The second number can\'t be zero.')
    except KeyboardInterrupt:
        print('\nYou pressed Ctrl+C')
        break
    finally:
        print('This is executed on every loop iteration.')
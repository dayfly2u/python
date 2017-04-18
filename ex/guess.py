import random

guess_made = 0

name = raw_input('hello what is your name?\n')
number = random.randint(1,20)
print 'well, {0}, I am thinking of a number between 1 and 20'.format(name)

while guess_made < 6:
    guess = int(raw_input('take a guess:'))
    guess_made += 1

    if guess < number:
        print 'your guess is too low'
    elif guess > number:
        print 'your guess is too high'
    else:
        break

if guess == number:
    print 'good job, {0}'.format(name)
else:
    print 'nope, the number I was thinking of was {0}'.format(number)


    

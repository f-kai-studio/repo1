# TRACKER
#### Video Demo:  https://youtu.be/ZPCFRO8E9ig
#### Description:
TRACKER is an expense tracker webapp that uses python for backend, CSS and jinjja for frontend programming. Inspired by Week 9's Finance pset, I made an expense tracker that allows users to note down their expenditure and income as well as to save their expense sheets to a log in order to refresh and start new expense sheets to the user's discretion. I decided on a pastel, video-game-like aesthetic for a soft appearance. Expense tracking and dealing with personal finances is stressful enough. app.py is where I store my main python code. index configures my home page, buy configures adding expenses, login and logout for their eponymous functions, register to register, update configures adding an income, log configures saving the current expense sheet, logged shows the history of expenses, and refresh clears the main expense sheet. login and logout are borrowed from Finance. helpers.py is borrowed and slightly modified from Finance so that I can use the login functionality. requirements.txt prescribes the packages on which the app depends - borrowed from Finance. tracker.db is the database where user information, the main expense sheet, and the log of expense sheets are stored. In the templates folder, I have apology, buy, index, layout, log, logged, login, refresh, register, and update. They all correspond to the various functions listed about that comprises the main python app routes. In the static folder I have the stylesheet and the icon borrowed from Finance. Finally, under flask_session, temp files of flask sessions are stored.

Overview for use: the dropdown navbar on the top left of the page, located next to the TRACKER logo, is your friend. Register for an account, login. Once logged in, use Add Income and Add expense to add items to your expense sheet as credit and debit inputs respectively. Once satisfied with the current expense sheet, hit 'save sheet' to log the main sheet in the history tab. Check in on saved sheets under the history tab. Then, once ready to start a new expense sheet, hit 'refresh'. Voila.

Directions for Use: To get started, register for an account. Type in a username and password, then confirm the password. You'll be directed to the homepage. There won't be much yet. Hit the dropdown bar and click 'add income'. You'll see four input boxes for Item Name, Dollar Amount, Quantity, and Category. Item name can be anything you want, but something like 'Paycheck' or 'Venmo from John' would make sense. Dollar amount takes a float value. Quantity is the multiple of the item, so if you input '2', the Dollar Amount you typed in will be doubled in the output later. Category is for your own housekeeping - keeping things consistent with categories makes it easy to keep track of your expenses - something like 'Salary' would make sense here.

Back at the homepage, you'll see that your income entry would have been added, with the 'NET' row under it also updating to show the total positive dollar amount you've added. More on NET later.

Now, click the dropdown bar again and click 'add expense'. Again, you'll see four boxes, this time for Item Name, Quantity, Category, and Price. Item Name, Quantity, and category work the same as before, while Price works the same as 'Dollar Amount' from before. In this case, Item Name could be something like 'Dinner' or 'Rent', Category could be 'Leisure' or 'Bills', and so on. Click Insert to add your entry.

See now that your expense entry is added, with the 'NET' row under it updating to show the balance of the 'total' amounts. 'Add Income' entries are recorded as a debit entry, hence they are a net positive; 'Add Expense' entries are recorded as a credit entry, hence they are a net negative. The NET row keeps track of that and calculates the balance, displaying your expense sheet total.

Once you are done with your expense sheet, perhaps for the month or for the quarter, you want to save it for future reference. Hit the dropdown and click 'Save Sheet'. You will be prompted to input the month and year by the app but this is just a suggestion for how to organise your saved sheet data. Once you key in your desired input, hit enter. Back at the home page nothing changes - but hit the dropdown again and click on 'history'. There, your data is saved.

Free now to refresh the sheet for a new use, click the big 'Refresh Sheet' button at the bottom of the page. You will be prompted to confirm refresh so that you dont delete your current sheet by accident. Once down, you'll have a fresh sheet for new use! Thank you for your time.
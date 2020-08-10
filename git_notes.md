## Git quick notes




**Show user of the repo**

`git config user.name`



**Show email of the repo**

`git config user.email`



**Setting user email to a repo**

`git config user.email "jonathanandrade10@gmail.com"`



**Setting user name to a repo**

`git config user.name "jonathanandrade10"`



**Remove last commit from origin(remote) repo**

`git push -f origin HEAD^:master`



**Commit setting author**

`git commit --author="jonathanandrade10@gmail.com<jonathanandrade10@gmail.com>" -m "Commit msg"`



**Change last commit message**

`git commit --amend -m "New commit message"`

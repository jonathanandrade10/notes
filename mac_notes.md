## Create variables on Mac

```vi ~/.bash_profile``` --old

```vi ~/.zprofile``` --actual

<br> reload the variables


```source ~/.bash_profile``` --old

```source ~/.zprofile``` --actual

## Mac Dev stuff

### Homebrew

install homebrew and apps

```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"```

``` brew install git openjdk openjdk@11 python ```


<br> View ``` brew info openjdk ``` for more details about Java setup and create a symbolic link.
 
>For the system Java wrappers to find this JDK, symlink it with
>  sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk


``` brew install --cask spotify slack zoom iterm2 ```


## Create SSH Keys

### ED25519 SSH keys

```ssh-keygen -t ed25519 -C "<comment>"```

```ssh-keygen -t ed25519``` - without comment by default the user@machine is set at the end of the key content.


**RSA SSH keys**

```ssh-keygen -t rsa -b 2048 -C "email@example.com"```


**Default folder to add ssh keys**

```/home/user/.ssh/id_rsa```

**Copy the key to the clipboard**

```pbcopy < ~/.ssh/id_ed25519.pub```

 
### <br>Having multiple keys u must create a config file

```
touch config
```

https://stackoverflow.com/questions/2419566/best-way-to-use-multiple-ssh-private-keys-on-one-client


```
Host myshortname realname.example.com
    HostName realname.example.com
    IdentityFile ~/.ssh/realname_rsa # private key for realname
    User remoteusername
  
Host myother realname2.example.org
    HostName realname2.example.org
    IdentityFile ~/.ssh/realname2_rsa  # different private key for realname2
    User remoteusername
```
    
    
**Git multiple keys config**

```
#git account  
Host git git-server.com  
AddKeysToAgent yes  
UseKeyChain yes  
HostName git-server.com  
User git  
IdentityFile ~/.ssh/id_rsa  
```

### <br>Testing git


```ssh -T git@git-server.com```

**Check if keys are loaded:**

```ssh-add -l```

**Add keys to agent:**

```
ssh-add <path_to_key> 
eg(ssh-add ~/.ssh/id_rsa)
```

## Create variables on Mac

```vi ~/.bash_profile``` --old

```vi ~/.zprofile``` --actual

<br> reload the variables


```source ~/.bash_profile``` --old

```source ~/.zprofile``` --actual


<br>This sets the environment for interactive shells

```vi ~/.zshrc```

## Mac Dev stuff

### Iterm

Go to Preferences... > Profiles > Keys (not Preferences... > Keys)
On current versions (3.14+) you then switch to the Key Mappings tab
Press Presets... dropdown button.
Select Natural Text Editing

https://apple.stackexchange.com/a/293988

### Pyenv

https://realpython.com/intro-to-pyenv/#installing-pyenv


### SDKMAN
https://sdkman.io/

```curl -s "https://get.sdkman.io" | bash```

**Scala** - ```sdk install scala 2.13.8```

### Homebrew

install homebrew and apps

```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"```

``` brew install git openjdk openjdk@11 python ```

**IntelliJ IDEA JDK Setup for homebrew users**
For anyone on a Mac with a homebrew-installed openjdk, you need to use the directory under libexec: <openjdk11_directory>/libexec/openjdk.jdk/Contents/Home. https://stackoverflow.com/a/69410018
Eg.:
``` /usr/local/Cellar/openjdk@8/1.8.0+322/libexec/openjdk.jdk/Contents/Home ```


<br> View ``` brew info openjdk ``` for more details about Java setup and create a symbolic link.
 
>For the system Java wrappers to find this JDK, symlink it with
>  sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

**Other things**
``` brew install --cask spotify slack zoom iterm2 ```

### Java and Scala versions on M1

homebrew jdk 8 doesn't support M1 -> https://formulae.brew.sh/formula/openjdk@8

but Java 11 does support M1 Apple Silicon -> https://formulae.brew.sh/formula/openjdk@11

For Scala 2.11 the documentation recommends the version 2.11.12, which is compatible with JDK 6, 7, 8 and 11 .
https://docs.scala-lang.org/overviews/jdk-compatibility/overview.html



### Git
git config --global user.name "Your Name“

git config --global user.email email@abc.com


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

**SSH key password on keychain**

```ssh-add --apple-use-keychain ~/.ssh/id_rsa```
 
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

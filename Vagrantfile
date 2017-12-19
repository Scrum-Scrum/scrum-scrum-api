# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "rustic/Fedora22"

  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080

  config.vm.provision "shell", inline: <<-SHELL
    # Set language
    sudo localectl set-locale LANG=en_US.UTF-8
    # Install Python
    sudo yum install -y python2.7 python-pip
    # Update pip
    sudo pip install --upgrade pip
    # Install MariaDB
    sudo yum -y install mysql-server mysql
    # Start MariaDB
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    # Install virtualenvwrapper
    sudo pip install virtualenvwrapper
    if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
      echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
      echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
      echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
      echo "source /usr/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
    fi
  SHELL
end

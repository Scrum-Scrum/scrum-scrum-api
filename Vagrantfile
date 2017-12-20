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
    sudo yum install -y python-devel python-pip
    # Update pip
    sudo pip install --upgrade pip
    # Install MariaDB
    sudo yum -y install mysql-server mysql
    if ! grep -q MYSQL_PATH_ALREADY_ADDED /home/vagrant/.bashrc; then
      echo "# MYSQL_PATH_ALREADY_ADDED" >> /home/vagrant/.bashrc
      echo "export PATH=$PATH:/usr/local/mysql/bin" >> /home/vagrant/.bashrc
    fi
    sudo yum -y install mysql-devel
    # sudo yum install MySQL-python
    # sudo pip install mysqlclient
    # Start MariaDB
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    # Install virtualenvwrapper
    sudo pip install virtualenvwrapper
    # Set up virtualenv 'scrum_scrum'
    if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
      echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
      echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
      echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
      echo "source /usr/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
      echo "mkvirtualenv scrum_scrum" >> /home/vagrant/.bashrc
    fi
    # Make sure the database is set up
    if ! grep -q MYSQL_PERMISSIONS_ALREADY_SET /home/vagrant/.bashrc; then
      echo "# MYSQL_PERMISSIONS_ALREADY_SET" >> /home/vagrant/.bashrc
      mysql -uroot -e "GRANT ALL ON *.* TO ''@'localhost'"
      mysql -e "CREATE DATABASE IF NOT EXISTS scrum_scrum"
    fi
  SHELL
end

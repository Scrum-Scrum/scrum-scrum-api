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

    # Install wget
    sudo dnf install -y wget

    # Install npm and nodejs
    sudo wget https://nodejs.org/download/release/v9.0.0/node-v9.0.0-linux-x64.tar.xz
    tar -xf node-v9.0.0-linux-x64.tar.xz --directory /home/vagrant --strip-components 1

    # Install MariaDB
    sudo dnf -y install mysql-server mysql

    if ! grep -q MYSQL_PATH_ALREADY_ADDED /home/vagrant/.bashrc; then
      echo "# MYSQL_PATH_ALREADY_ADDED" >> /home/vagrant/.bashrc
      echo "export PATH=$PATH:/usr/local/mysql/bin" >> /home/vagrant/.bashrc
    fi

    sudo dnf -y install mysql-devel

    # Start MariaDB
    sudo systemctl start mariadb
    sudo systemctl enable mariadb

    # Make sure the database is set up
    if ! grep -q MYSQL_PERMISSIONS_ALREADY_SET /home/vagrant/.bashrc; then
      echo "# MYSQL_PERMISSIONS_ALREADY_SET" >> /home/vagrant/.bashrc
      mysql -uroot -e "GRANT ALL ON *.* TO ''@'localhost'"
      mysql -e "CREATE DATABASE IF NOT EXISTS scrum_scrum"
    fi
    # Configure the virtual machine's firewall to allow networking requests
    if ! grep -q FIREWALL_CONFIGURED /home/vagrant/.bashrc; then
      echo "# FIREWALL_CONFIGURED" >> /home/vagrant/.bashrc
      sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent
      sudo firewall-cmd --reload
    fi
  SHELL
end

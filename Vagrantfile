# -*- mode: ruby -*-
# vi: set ft=ruby :

# Get the number of web nodes to start up, defaults to 3
web_nodes = ENV['WEB_NODES_NUMBER'].to_i || 3

Vagrant.configure(2) do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "https://files.hashicorp.com/precise32.box"
  config.vm.provider :virtualbox do |vb|
    # Use host's DNS resolver to ensure it works in all cases
    # https://www.virtualbox.org/manual/ch09.html#nat_host_resolver_proxy
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # The webnode(s)
  (1..web_nodes).each do |i|
    config.vm.define "web-node-#{i}" do |node|
      node.vm.hostname = "web-node-#{i}"
      node.vm.network :private_network, ip: "192.168.0.#{i+9}"
      node.vm.synced_folder "webpage", "/wwwroot", owner: "www-data", group: "www-data"
      node.vm.provider :virtualbox do |vb|
        # Set a "nice" name in VirtualBox gui
        vb.name = "web-node-#{i}"
      end
      # Vagrant do not manage to install ansible with ansible=true for precies32 box
      node.vm.provision "shell", inline: "apt-get update && apt-get install -y ansible"
      node.vm.provision "ansible_local" do |ansible|
        ansible.install = true
        ansible.playbook = "ansible/main.yml"
        ansible.groups = {
          "webservers" => ["web-node-[1:#{web_nodes}]"]
        }
      end
    end
  end

  # The loadbalancer
  config.vm.define "lb-web-node-1" do |lb|
    lb.vm.hostname = "lb-web-node-1"
    lb.vm.network :private_network, ip: "192.168.0.5"
    lb.vm.provider :virtualbox do |vb|
      # Set a "nice" name in VirtualBox gui
      vb.name = "lb-web-node-1"
    end
    # Vagrant do not manage to install ansible with ansible=true for precies32 box
    lb.vm.provision "shell", inline: "apt-get update && apt-get install -y ansible"
    lb.vm.provision "ansible_local" do |ansible|
      ansible.install = true
      ansible.playbook = "ansible/main.yml"
      ansible.groups = {
        "loadbalancers" => ["lb-web-node-1"],
        "webservers" => ["192.168.0.[10:#{web_nodes+9}]"]
      }
    end
  end

end
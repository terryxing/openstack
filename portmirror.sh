ovs-vsctl  -- --id=@vm3 get port tap0cdb8e01-88 -- --id=@vm4 get port tapa0a5bd27-98 -- set Bridge br-int mirrors=@m  -- --id=@m create mirror name=mirror1 select-dst-port=@vm4 select-src-port=@vm4 output-port=@vm3


ovs-vsctl -- --id=@p get port tap9fdc1244-74 -- --id=@vm2 get port tap9b352673-75  -- add bridge br-int mirrors @m -- --id=@m create mirror name=mirrirvm12 select-dst-port=@vm2 select-src-port=@vm2 output-port=@pi

ovs-vsctl clear Bridge br-int mirrors



#flow table operation

ovs-ofctl add-flow br-int "dl_src=fa:16:3e:04:3e:89,priority=100,actions=NORMAL,mod_dl_dst=fa:16:3e:3d:1e:d8,NORMAL"

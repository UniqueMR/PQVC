- scale-up 纵向扩展：增强单个服务器节点性能；通常意味着给一个节点增加更多的CPU、内存、GPU或者更快的内部组件；通信主要发生在节点内部的组件之间
    - Nvidia：NVLink提供比PCIe总线更高的带宽，NVSwitch构建复杂节点的节点内拓扑，实现节点内所有GPU之间的全带宽通信
    - AMD: Infinity Fabric/xGMI

- scale-out 横向扩展：通过增加更多服务器节点，将它们连接起来协同工作；通信主要发生在节点之间，通过网络进行
    - InfiniBand使用Nvidia的ConnectX系列NICs + Ethernet使用Nvidia的ConnectX或BlueField系列NICs + Spectrum-X，针对AI优化的以太网解决方案，提供拥塞控制和自适应路由
    - AMD: Standard Ethernet（RoCEv2: RDMA over Converged Ethernet）并搭配Broadcom Thor-2 NICs；缺乏类似InfiniBand SHARP或Spectrum-X深度集成的独有网内计算或高度优化的网络解决方案

AMD即将推出Pollara 400G NIC，支持Ultra Ethernet(UEC)标准
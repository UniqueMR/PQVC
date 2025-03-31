block-beta
    columns 1
    block: C["业务板块层"]
        columns 4
        C1["数据中心"]
        C2["客户端"]
        C3["游戏"]
        C4["嵌入式"]
        style C fill:#eca8a9,stroke:#333,stroke-width:2px,rx:4,ry:4
        style C1 fill:#f5d5d6,stroke:#333,stroke-width:1px,rx:3,ry:3
        style C2 fill:#f5d5d6,stroke:#333,stroke-width:1px,rx:3,ry:3
        style C3 fill:#f5d5d6,stroke:#333,stroke-width:1px,rx:3,ry:3
        style C4 fill:#f5d5d6,stroke:#333,stroke-width:1px,rx:3,ry:3
    end
    block: B["产品系列层"]
        columns 5
        B1["Ryzen CPU"]
        B2["EPYC CPU"]
        B3["Radeon GPU"]
        B4["Instinct AI/HPC"]
        block: B5
            B51["Versal"]
            B52["Ultrascale"]
            B53["Zynq"]
        end
        style B fill:#74aed4,stroke:#333,stroke-width:2px,rx:4,ry:4
        style B1 fill:#b3d7e9,stroke:#333,stroke-width:1px,rx:3,ry:3
        style B2 fill:#b3d7e9,stroke:#333,stroke-width:1px,rx:3,ry:3
        style B3 fill:#b3d7e9,stroke:#333,stroke-width:1px,rx:3,ry:3
        style B4 fill:#b3d7e9,stroke:#333,stroke-width:1px,rx:3,ry:3
        style B5 fill:#b3d7e9,stroke:#333,stroke-width:1px,rx:3,ry:3
    end
    block: A["技术基础层"]
        columns 5
        A1["Zen架构"]
        block: A2
            A21["RDNA架构"]
            A22["CDNA架构"]
        end
        A3["FPGA & SoCs"]
        A4["ROCm软件生态"]
        style A fill:#d3e2b7,stroke:#333,stroke-width:2px,rx:4,ry:4
        style A1 fill:#e9f0db,stroke:#333,stroke-width:1px,rx:3,ry:3
        style A2 fill:#e9f0db,stroke:#333,stroke-width:1px,rx:3,ry:3

        style A3 fill:#e9f0db,stroke:#333,stroke-width:1px,rx:3,ry:3
        style A4 fill:#e9f0db,stroke:#333,stroke-width:1px,rx:3,ry:3
    end
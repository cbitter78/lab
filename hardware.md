# Lab Hardware

This is a list of the hardware I used to create this lab.  It was sourced from Amazon and NewEgg.

## Network


- [Switch](https://www.amazon.com/dp/B00AUEYXIG/ref=wl_it_dp_o_pC_S_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IM1XKPH4LNHFW&psc=1): This Netgear will support VLAN and VLAN trunking.  Its not super easy to use and the UI frankly sucks.  It is relatively inexpensive and is sielent.
- [Dumb Switch](https://www.amazon.com/dp/B00MPVR50A/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I3HFMAJKXJBFS1&psc=1) (optional): I used this so I only had one cable running from the lab to my house router.
- Cables: I used two colors [Green](https://www.amazon.com/dp/B0186AJ5VK/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IKHDLI3GSHTGN&psc=1) for Control Plane and [Orange](https://www.amazon.com/dp/B017C183EO/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I27ZM2YQZXD1RV&psc=1) Data Plane.

## Servers

### Open Stack Servers

I used [Gigabyte Intel i3-4010U Mini PC](https://www.amazon.com/dp/B00I05NH9S/ref=wl_it_dp_o_pC_S_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IZH8F8AXHKY38) 
chassie for both Control and Compute.   These come with everyting but the Memory and Hardrive.

I also added a [USB nic](https://www.amazon.com/dp/B00PIW2I96/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I2339SNCTAFZVH) to complement the existing network interface to bring the nic count to 2. (they do have a wireless interface I ignrored / disabled)

#### Control Plane

The three Control hosts use have a [60 GB SSD](https://www.amazon.com/dp/B00COFMPAM/ref=wl_it_dp_o_pd_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IILRQVRCOPBO1&psc=1) drive and [8 Gigs of Ram](https://www.amazon.com/dp/B012TS9UOM/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IF2LGK9HKE96E&psc=1) 


#### Compute Nodes

The two Compute nodes have [60 GB SSD](https://www.amazon.com/dp/B00COFMPAM/ref=wl_it_dp_o_pd_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IILRQVRCOPBO1&psc=1) drive another [240 GB SSD](https://www.amazon.com/dp/B00A1ZTZNM/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I21Z7XUYOMSNLI&psc=1) drive and [8 Gigs of Ram](https://www.amazon.com/dp/B012TS9UOM/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=IF2LGK9HKE96E&psc=1).  In retrospect I think the compute hosts only need the 60 GB drive. 


### Jump Host / PXE Server / Ansible Server / Whatever

I used a [Kangaroo](http://www.newegg.com/Product/Product.aspx?Item=N82E16883722001&nm_mc=KNC-GoogleKWLess&cm_mmc=KNC-GoogleKWLess-_-DSA-_-CategoryPages-_-NA&gclid=COH6n-H3uc0CFVAvgQodbrEKjA&gclsrc=aw.ds) for this host.   Its very small and only $99.00.  The Kangaroo will accept ubuntu 16.04 without issue.  I also added 2 [USB nic](https://www.amazon.com/dp/B00PIW2I96/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I2339SNCTAFZVH) to provide wired access.  One connects to the contrl plane network and the other to my home network.  This hosts provides a NAT between the two.

To make the USB Nics work I also picked up this [USB Hub](https://www.amazon.com/dp/B00KOHQU58/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I1F2RU5V64W9W2)

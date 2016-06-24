# Lab Hardware

This is a list of the hardware I used to create this lab.  It was sourced from Amazon with one exception of the [Kangaroo](http://www.newegg.com/Product/Product.aspx?Item=N82E16883722001&nm_mc=KNC-GoogleKWLess&cm_mmc=KNC-GoogleKWLess-_-DSA-_-CategoryPages-_-NA&gclid=COH6n-H3uc0CFVAvgQodbrEKjA&gclsrc=aw.ds) from NewEgg.

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

I also picked up this [SD Card](https://www.amazon.com/dp/B00M55C0NS/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I36NS8RZMZ9R5K&psc=1) to put the ubuntu-15.10 boot media on to make installing ubuntu easy on the Kangaroo.

## Other stuff

This is the other stuff I picked up just for FYI

- [Power Supply](https://www.amazon.com/dp/B01198B942/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=INTT0GKSJBPN2&psc=1)
- [Shelvs](https://www.amazon.com/dp/B013AN3XDE/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I3T0VD8XKP704K&psc=1)
- [Mouse](https://www.amazon.com/dp/B017VZR2SY/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I6H1OYO8Q3DCI)
- [Keyboard](https://www.amazon.com/dp/B005DPF08E/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I1OCRJHRLAFB7G)
- [Cable Management](https://www.amazon.com/dp/B00008VFAP/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I6HJO7OP6D0S0&psc=1)
- [Monitor wall mount](https://www.amazon.com/dp/B003O1UYHG/ref=wl_it_dp_o_pC_nS_ttl?_encoding=UTF8&colid=2IO0VDDWS55XY&coliid=I1YGOF0ZOBJ5DU)

Most everthing can be found on this [Amazon List](https://amzn.com/w/2IO0VDDWS55XY)

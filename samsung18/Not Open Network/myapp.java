
/*
 * Copyright 2018-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.example.myapp;


import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;
import org.apache.felix.scr.annotations.Service;

import org.onlab.packet.Ethernet;
import org.onlab.packet.IPv4;
import org.onlab.packet.TCP;

import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.Host;
import org.onosproject.net.HostId;
import org.onosproject.net.Path;
import org.onosproject.net.PortNumber;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.TrafficSelector;
import org.onosproject.net.flow.TrafficTreatment;
import org.onosproject.net.host.HostService;
import org.onosproject.net.packet.InboundPacket;
import org.onosproject.net.packet.OutboundPacket;
import org.onosproject.net.packet.DefaultOutboundPacket;
import org.onosproject.net.packet.PacketContext;
import org.onosproject.net.packet.PacketProcessor;
import org.onosproject.net.packet.PacketPriority;
import org.onosproject.net.packet.PacketService;
import org.onosproject.net.topology.TopologyService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(immediate = true)
public class AppComponent {

    private final Logger log = LoggerFactory.getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected HostService hostService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected PacketService packetService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected TopologyService topologyService;

    private ApplicationId appId;
    private MyPacketProcessor processor = new MyPacketProcessor();

    @Activate
    protected void activate() {
        // Print log to the ONOS screen.
        log.info("Started");
        appId = coreService.registerApplication("com.example.myapp");

        // Make all IPv4 packets to pass through this app.
        packetService.addProcessor(processor, PacketProcessor.director(2));
        TrafficSelector selector = DefaultTrafficSelector.builder()
            .matchEthType(Ethernet.TYPE_IPV4)
            .build();
        packetService.requestPackets(selector, PacketPriority.REACTIVE, appId);
    }

    @Deactivate
    protected void deactivate() {
        log.info("Stopped");
        if (processor != null) {
            packetService.removeProcessor(processor);
            processor = null;
        }
    }

    private class MyPacketProcessor implements PacketProcessor {
        // This method is invoked whenever we receive a packet
        // that is not matched in the routing tables.
        @Override
        public void process(PacketContext context) {
            // Return if another app has already dealt with this packet.
            if (context.isHandled())
                return;

            InboundPacket pkt = context.inPacket();
            Ethernet ethPkt = pkt.parsed();
            if (ethPkt == null)
                return;
            allowPacket(context, ethPkt);
        }

        private void allowPacket(PacketContext context, Ethernet ethPkt) {
        	try {

	        	byte[] ipv4Buf = ethPkt.serialize();
	        	// IPv4 헤더 생성
                IPv4 ipv4Pkt = IPv4.deserializer().deserialize(ipv4Buf,14,ipv4Buf.length-14);
                // 해당 패킷이 TCP이면 비교를 수행한다. 다만 서버 IP 대역인 10.0.0.0/16은 예외처리한다.
	        	if (ipv4Pkt.getProtocol() == IPv4.PROTOCOL_TCP && (ipv4Pkt.getSourceAddress() & 0xFFFF0000) != 0x0a000000 )
	        	{
	        		byte[] tcpBuf = ipv4Pkt.serialize();
	        		int hsize = (int)ipv4Pkt.getHeaderLength() * 4;
	        		// TCP 헤더 생성 
	        		TCP tcpPkt = TCP.deserializer().deserialize(tcpBuf,hsize,tcpBuf.length-hsize);
                    // 80 포트가 맞는가?
	        		if(tcpPkt.getDestinationPort() != 80)
	        		{
	        		//	log.info("NO 80 port");
	        			context.block();
	        			return;
	        		}
                    // TCP 해더와 DATA를 문자열화
	        		//int tsize = (int)tcpPkt.getDataOffset() * 4;
	        		byte[] binBuf = tcpPkt.serialize();
	        		String binBuf2 = new String(binBuf,0,binBuf.length);
                    // case insensitive를 위한 toLowerCase 그리고 police 문자열 포함 확인
	        		if(binBuf2.toLowerCase().indexOf("police") != -1)
	        		{
	        		//	log.info("NO police!");
	        			context.block();
	        			return;
	        		}
	        		//log.info("PASS");

	        	}
	        } catch (Exception dex) {
	        	throw new IllegalStateException(dex);
			}
            HostId dstId = HostId.hostId(ethPkt.getDestinationMAC());
            Host dst = hostService.getHost(dstId);
            // If we don't know where it's heading for, just broadcast it.
            if (dst == null) {
                if (topologyService.isBroadcastPoint(
                            topologyService.currentTopology(),
                            context.inPacket().receivedFrom())) {
                    context.treatmentBuilder().setOutput(PortNumber.FLOOD);
                    context.send();
                }
                else {
                    context.block();
                }
            }
            // Forward packet to its destination.
            else {
                TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                    .setOutput(dst.location().port())
                    .build();
                OutboundPacket packet = new DefaultOutboundPacket(
                        dst.location().deviceId(),
                        treatment,
                        context.inPacket().unparsed());
                packetService.emit(packet);
            }
        }
    }
}

from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY_TYPE = 0
ICMP_ECHO_REPLY_CODE = 0
ICMP_ERROR_TYPE = 3
ICMP_DEST_NET_UNREACHABLE_CODE = 0
ICMP_DEST_HOST_UNREACHABLE_CODE = 1
ICMP_DEST_PROTO_UNREACHABLE_CODE = 2
ICMP_DEST_PORT_UNREACHABLE_CODE = 3
ICMP_DEST_NET_UNKNOWN_CODE = 6
ICMP_DEST_HOST_UNKNOWN_CODE = 7


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + (string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if not whatReady[0]:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # fill in start
        ipHeader = recPacket[:20]
        icmpHeader = recPacket[20:28]
        packetData = recPacket[28:]

        ipVersion, ipTypeOfSvc, ipLength, ipID, ipFlags, ipTTL, ipProtocol, ipChecksum, ipSrcIP, ipDestIP = struct.unpack(
            "!BBHHHBBHII", ipHeader)
        icmpType, icmpCode, icmpChecksum, packetID, packetSequence = struct.unpack('bbHHh', icmpHeader)

        if len(packetData) == 8:
            timeSent = struct.unpack('d', packetData)[0]
        else:
            timeSent = None

        expectedIcmpChecksum = 0
        # Make a dummy header with a 0 checksum
        # struct -- Interpret strings as packed binary data
        header_checksum = struct.pack("bbHHh", icmpType, icmpCode, expectedIcmpChecksum, packetID, packetSequence)
        if len(packetData) == 8:
            data_checksum = struct.pack("d", timeSent)
        else:
            data_checksum = bytes()
        # Calculate the checksum on the data and the dummy header.
        expectedIcmpChecksum = checksum(header_checksum + data_checksum)

        # Get the right checksum, and put in the header
        if sys.platform == 'darwin':
            # Convert 16-bit integers from host to network  byte order
            expectedIcmpChecksum = htons(expectedIcmpChecksum) & 0xffff
        else:
            expectedIcmpChecksum = htons(expectedIcmpChecksum)

        if addr[0] == destAddr and icmpType == ICMP_ECHO_REPLY_TYPE and icmpCode == ICMP_ECHO_REPLY_CODE and \
                packetID == ID and packetSequence == 1 and icmpChecksum == expectedIcmpChecksum:
            # Return the RTT in ms
            rtt = (timeReceived - timeSent) * 1000.0
            return '{0}: ICMP seq={1} TTL={2} RTT={3:.3f}ms'.format(addr[0], packetSequence, ipTTL, rtt), rtt
        elif icmpType == ICMP_ERROR_TYPE and icmpCode == ICMP_DEST_NET_UNREACHABLE_CODE and \
                icmpChecksum == expectedIcmpChecksum:
            return 'Destination network unreachable.', 'na'
        elif icmpType == ICMP_ERROR_TYPE and icmpCode == ICMP_DEST_HOST_UNREACHABLE_CODE and \
                icmpChecksum == expectedIcmpChecksum:
            return 'Destination host unreachable.', 'na'
        elif icmpType == ICMP_ERROR_TYPE and icmpCode == ICMP_DEST_PROTO_UNREACHABLE_CODE and \
                icmpChecksum == expectedIcmpChecksum:
            return 'Destination protocol unreachable.', 'na'
        elif icmpType == ICMP_ERROR_TYPE and icmpCode == ICMP_DEST_PORT_UNREACHABLE_CODE and \
                icmpChecksum == expectedIcmpChecksum:
            return 'Destination port unreachable.', 'na'
        elif icmpType == ICMP_ERROR_TYPE and icmpCode == ICMP_DEST_NET_UNKNOWN_CODE and \
                icmpChecksum == expectedIcmpChecksum:
            return 'Destination network unknown.', 'na'
        elif icmpType == ICMP_ERROR_TYPE and icmpCode == ICMP_DEST_HOST_UNKNOWN_CODE and \
                icmpChecksum == expectedIcmpChecksum:
            return 'Destination host unknown.', 'na'
        # fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # Create Socket here
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    dest = gethostbyname(host)

    print("Pinging " + dest + " using Python:")
    print("")

    # Send ping requests to a server separated by approximately one second
    while 1:
        print(doOnePing(dest, timeout))
        print()
        time.sleep(1)  # one second


print("Ping to google")
ping("google.com")

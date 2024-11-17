import React, { useState } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Text,
  Badge,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  VStack,
  Input,
  useToast
} from '@chakra-ui/react';

// Mock de pedidos para demostración
const mockOrders = [
  {
    id: "ORD-001",
    date: "2024-01-15",
    total: 1299.99,
    status: "Entregado",
    tracking: "1Z999AA1234567890",
    items: [
      {
        id: 1,
        name: "Laptop Gaming Pro",
        price: 1299.99,
        quantity: 1
      }
    ]
  },
  {
    id: "ORD-002",
    date: "2024-01-16",
    total: 899.99,
    status: "En tránsito",
    tracking: "1Z999AA1234567891",
    items: [
      {
        id: 2,
        name: "Smartphone Ultra",
        price: 899.99,
        quantity: 1
      }
    ]
  }
];

export const OrderHistory = () => {
  const [orders] = useState(mockOrders);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [trackingInput, setTrackingInput] = useState("");
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();

  // Vulnerable: No validación de entrada para el número de seguimiento
  const trackOrder = () => {
    // Vulnerable: Inyección SQL potencial
    const query = `SELECT * FROM orders WHERE tracking_number = '${trackingInput}'`;

    // Vulnerable: Almacenamiento de datos sensibles sin encriptación
    localStorage.setItem('lastTracking', trackingInput);

    // Vulnerable: Ejecución de código arbitrario
    const trackingScript = localStorage.getItem('trackingScript');
    if (trackingScript) {
      eval(trackingScript);
    }

    toast({
      title: "Rastreando pedido",
      description: `Número de seguimiento: ${trackingInput}`,
      status: "info",
      duration: 3000,
      isClosable: true,
    });
  };

  // Vulnerable: No validación de entrada para el ID del pedido
  const viewOrderDetails = (order) => {
    setSelectedOrder(order);
    // Vulnerable: Registro de información sensible en console.log
    console.log('Detalles del pedido:', order);
    onOpen();
  };

  // Vulnerable: No validación de entrada para el cupón
  const applyCoupon = (orderId, coupon) => {
    // Vulnerable: Inyección de código en el manejo de cupones
    const discountScript = `
      const discount = calculateDiscount('${coupon}');
      applyDiscount(${orderId}, discount);
    `;
    eval(discountScript);
  };

  return (
    <Box p={4}>
      <Text fontSize="2xl" mb={4}>Historial de Pedidos</Text>

      <VStack spacing={4} mb={6}>
        <Input
          placeholder="Ingrese número de seguimiento"
          value={trackingInput}
          onChange={(e) => setTrackingInput(e.target.value)}
        />
        <Button colorScheme="blue" onClick={trackOrder}>
          Rastrear Pedido
        </Button>
      </VStack>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>ID Pedido</Th>
            <Th>Fecha</Th>
            <Th>Total</Th>
            <Th>Estado</Th>
            <Th>Acciones</Th>
          </Tr>
        </Thead>
        <Tbody>
          {orders.map((order) => (
            <Tr key={order.id}>
              <Td>{order.id}</Td>
              <Td>{order.date}</Td>
              <Td>${order.total}</Td>
              <Td>
                <Badge
                  colorScheme={order.status === "Entregado" ? "green" : "yellow"}
                >
                  {order.status}
                </Badge>
              </Td>
              <Td>
                <Button
                  size="sm"
                  onClick={() => viewOrderDetails(order)}
                >
                  Ver Detalles
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Detalles del Pedido {selectedOrder?.id}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {selectedOrder && (
              <VStack align="stretch" spacing={4}>
                <Text>Fecha: {selectedOrder.date}</Text>
                <Text>Estado: {selectedOrder.status}</Text>
                <Text>Número de Seguimiento: {selectedOrder.tracking}</Text>
                <Text fontWeight="bold">Productos:</Text>
                {selectedOrder.items.map((item) => (
                  <Box key={item.id} p={2} borderWidth={1} borderRadius="md">
                    <Text>{item.name}</Text>
                    <Text>Cantidad: {item.quantity}</Text>
                    <Text>Precio: ${item.price}</Text>
                  </Box>
                ))}
                <Text fontWeight="bold">Total: ${selectedOrder.total}</Text>

                <Input
                  placeholder="Ingrese código de cupón"
                  onChange={(e) => applyCoupon(selectedOrder.id, e.target.value)}
                />
              </VStack>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

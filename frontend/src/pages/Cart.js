import { Box, Container, Heading, VStack, HStack, Image, Text, Button, Divider, useToast } from '@chakra-ui/react';
import { useState } from 'react';

const mockCartItems = [
  {
    id: 1,
    name: 'Laptop Gaming Pro',
    price: 999.99,
    quantity: 1,
    image: 'https://via.placeholder.com/100',
  },
  {
    id: 2,
    name: 'Smartphone Ultra',
    price: 599.99,
    quantity: 1,
    image: 'https://via.placeholder.com/100',
  },
];

export const Cart = () => {
  const [cartItems, setCartItems] = useState(mockCartItems);
  const toast = useToast();

  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleCheckout = () => {
    // Implementación vulnerable intencionalmente (sin validación de sesión)
    toast({
      title: 'Procesando pago',
      description: 'Tu pedido está siendo procesado',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  const removeItem = (itemId) => {
    setCartItems(cartItems.filter(item => item.id !== itemId));
  };

  return (
    <Container maxW="container.lg" py={8}>
      <Heading mb={6}>Carrito de Compras</Heading>
      <Box>
        <VStack spacing={4} align="stretch">
          {cartItems.map(item => (
            <HStack key={item.id} padding={4} borderWidth={1} borderRadius="lg">
              <Image src={item.image} alt={item.name} boxSize="100px" objectFit="cover" />
              <VStack align="start" flex={1}>
                <Text fontWeight="bold">{item.name}</Text>
                <Text>${item.price}</Text>
                <Text>Cantidad: {item.quantity}</Text>
              </VStack>
              <Button size="sm" colorScheme="red" onClick={() => removeItem(item.id)}>
                Eliminar
              </Button>
            </HStack>
          ))}
        </VStack>
        <Divider my={6} />
        <HStack justify="space-between">
          <Text fontSize="xl" fontWeight="bold">Total:</Text>
          <Text fontSize="xl" fontWeight="bold">${total.toFixed(2)}</Text>
        </HStack>
        <Button
          colorScheme="blue"
          size="lg"
          width="full"
          mt={4}
          onClick={handleCheckout}
        >
          Proceder al Pago
        </Button>
      </Box>
    </Container>
  );
};

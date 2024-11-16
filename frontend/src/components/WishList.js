import React, { useState } from 'react';
import {
  Box,
  Text,
  Button,
  SimpleGrid,
  Image,
  VStack,
  useToast,
  IconButton
} from '@chakra-ui/react';
import { DeleteIcon } from '@chakra-ui/icons';

// Componente vulnerable que almacena datos sensibles en localStorage sin encriptación
export const WishList = () => {
  const [wishList, setWishList] = useState(() => {
    // Vulnerable: Datos almacenados sin encriptación en localStorage
    const savedWishList = localStorage.getItem('wishList');
    return savedWishList ? JSON.parse(savedWishList) : [
      {
        id: 1,
        name: "Laptop Gaming Pro",
        price: 1299.99,
        image: "https://source.unsplash.com/random/200x200?laptop",
      },
      {
        id: 2,
        name: "Smartphone Ultra",
        price: 899.99,
        image: "https://source.unsplash.com/random/200x200?smartphone",
      }
    ];
  });

  const toast = useToast();

  // Vulnerable: No validación de datos antes de guardar
  const removeFromWishList = (productId) => {
    const updatedWishList = wishList.filter(item => item.id !== productId);
    setWishList(updatedWishList);
    // Vulnerable: Almacenamiento directo sin validación
    localStorage.setItem('wishList', JSON.stringify(updatedWishList));

    toast({
      title: "Producto eliminado de la lista de deseos",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  const addToCart = (product) => {
    // Vulnerable: Inyección de datos directa al carrito
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));

    toast({
      title: "Producto agregado al carrito",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box p={4}>
      <Text fontSize="2xl" mb={4}>Mi Lista de Deseos</Text>
      <SimpleGrid columns={[1, 2, 3]} spacing={4}>
        {wishList.map((product) => (
          <Box
            key={product.id}
            borderWidth={1}
            borderRadius="lg"
            overflow="hidden"
            p={4}
          >
            <Image
              src={product.image}
              alt={product.name}
              borderRadius="md"
              mb={4}
            />
            <VStack align="start" spacing={2}>
              <Text fontWeight="bold">{product.name}</Text>
              <Text color="blue.600">${product.price}</Text>
              <Button
                colorScheme="blue"
                size="sm"
                onClick={() => addToCart(product)}
                width="full"
              >
                Agregar al Carrito
              </Button>
              <IconButton
                aria-label="Eliminar de la lista"
                icon={<DeleteIcon />}
                onClick={() => removeFromWishList(product.id)}
                colorScheme="red"
                size="sm"
                width="full"
              />
            </VStack>
          </Box>
        ))}
      </SimpleGrid>
    </Box>
  );
};

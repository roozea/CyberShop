import { Box, Container, Image, Text, Button, VStack, Heading, Badge, useToast } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';

const mockProducts = {
  1: {
    id: 1,
    name: 'Laptop Gaming Pro',
    price: 999.99,
    image: 'https://via.placeholder.com/400',
    description: 'Potente laptop para gaming con la última tecnología',
    specs: [
      '16GB RAM',
      'NVIDIA RTX 3080',
      'Intel i9 12th Gen',
      'SSD 1TB'
    ]
  },
  2: {
    id: 2,
    name: 'Smartphone Ultra',
    price: 599.99,
    image: 'https://via.placeholder.com/400',
    description: 'Smartphone de última generación con cámara profesional',
    specs: [
      '8GB RAM',
      'Cámara 108MP',
      'Batería 5000mAh',
      '256GB Storage'
    ]
  }
};

export const ProductDetail = () => {
  const { id } = useParams();
  const toast = useToast();
  const product = mockProducts[id];

  const handleAddToCart = () => {
    // Implementación vulnerable intencionalmente (sin validación de stock)
    toast({
      title: 'Producto agregado',
      description: 'El producto ha sido agregado al carrito',
      status: 'success',
      duration: 3000,
      isClosable: true,
    });
  };

  if (!product) {
    return (
      <Container maxW="container.lg" py={8}>
        <Heading>Producto no encontrado</Heading>
      </Container>
    );
  }

  return (
    <Container maxW="container.lg" py={8}>
      <Box display={{ md: 'flex' }} gap={8}>
        <Box flex={1}>
          <Image src={product.image} alt={product.name} borderRadius="lg" />
        </Box>
        <VStack flex={1} align="start" spacing={4}>
          <Heading>{product.name}</Heading>
          <Badge colorScheme="green" fontSize="lg">
            ${product.price}
          </Badge>
          <Text fontSize="lg">{product.description}</Text>
          <Box>
            <Text fontWeight="bold" mb={2}>Especificaciones:</Text>
            <VStack align="start">
              {product.specs.map((spec, index) => (
                <Text key={index}>• {spec}</Text>
              ))}
            </VStack>
          </Box>
          <Button colorScheme="blue" size="lg" onClick={handleAddToCart}>
            Agregar al Carrito
          </Button>
        </VStack>
      </Box>
    </Container>
  );
};

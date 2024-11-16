import { Box, Image, Badge, Text, Button, Flex } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

export const ProductCard = ({ product }) => {
  return (
    <Box maxW="sm" borderWidth="1px" borderRadius="lg" overflow="hidden">
      <Image src={product.image} alt={product.name} />

      <Box p="6">
        <Box display="flex" alignItems="baseline">
          <Badge borderRadius="full" px="2" colorScheme="teal">
            Nuevo
          </Badge>
        </Box>

        <Box mt="1" fontWeight="semibold" as="h4" lineHeight="tight">
          {product.name}
        </Box>

        <Box>
          ${product.price}
        </Box>

        <Flex mt={4} justify="space-between" align="center">
          <Link to={`/product/${product.id}`}>
            <Button variant="outline" colorScheme="blue">
              Ver detalles
            </Button>
          </Link>
          <Button colorScheme="blue">
            Agregar al carrito
          </Button>
        </Flex>
      </Box>
    </Box>
  );
};

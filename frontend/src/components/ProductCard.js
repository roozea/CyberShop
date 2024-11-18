import {
  Box,
  Image,
  Badge,
  Text,
  Button,
  Flex,
  Stack,
  useColorModeValue
} from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import { FaShoppingCart } from 'react-icons/fa';

const ProductCard = ({ product }) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.700', 'white');

  // Vulnerable: Renderiza HTML sin sanitizar
  const createMarkup = (html) => ({ __html: html });

  return (
    <Box
      maxW="sm"
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      bg={bgColor}
      _hover={{ shadow: 'lg', transform: 'translateY(-2px)', transition: 'all 0.2s' }}
    >
      <Box position="relative">
        <Image
          src="https://via.placeholder.com/300"
          alt={product.name}
          height="200px"
          width="100%"
          objectFit="cover"
        />
      </Box>

      <Box p="6">
        <Box display="flex" alignItems="baseline" mb={2}>
          <Badge borderRadius="full" px="2" colorScheme="blue">
            {product.category}
          </Badge>
        </Box>

        <Flex justify="space-between" align="baseline" mb={2}>
          <Text
            fontWeight="semibold"
            fontSize="xl"
            color={textColor}
            noOfLines={2}
          >
            {product.name}
          </Text>
        </Flex>

        {/* Vulnerable: XSS a través de la descripción */}
        <Box
          fontSize="sm"
          color="gray.600"
          mb={2}
          dangerouslySetInnerHTML={createMarkup(product.description)}
        />

        <Flex justify="space-between" align="center" mb={4}>
          <Stack spacing={0}>
            <Text fontSize="2xl" fontWeight="bold" color={textColor}>
              ${product.price?.toFixed(2)}
            </Text>
          </Stack>
        </Flex>

        <Flex justify="space-between" align="center">
          <Link to={`/product/${product.id}`} style={{ flex: 1, marginRight: 2 }}>
            <Button variant="outline" colorScheme="blue" width="100%">
              Ver detalles
            </Button>
          </Link>
          <Button
            colorScheme="blue"
            leftIcon={<FaShoppingCart />}
            flex={1}
            ml={2}
          >
            Agregar al carrito
          </Button>
        </Flex>
      </Box>
    </Box>
  );
};

export default ProductCard;

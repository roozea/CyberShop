import {
  Box,
  Image,
  Badge,
  Text,
  Button,
  Flex,
  Stack,
  Icon,
  Tooltip,
  useColorModeValue
} from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import { FaStar, FaShoppingCart, FaHeart } from 'react-icons/fa';
import { BsBoxSeam } from 'react-icons/bs';

export const ProductCard = ({ product, onAddToCart }) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.700', 'white');

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
          src={product.image}
          alt={product.name}
          height="200px"
          width="100%"
          objectFit="cover"
        />
        {product.discount > 0 && (
          <Badge
            position="absolute"
            top="4"
            right="4"
            px="2"
            py="1"
            colorScheme="red"
            borderRadius="md"
            fontSize="sm"
            fontWeight="bold"
          >
            {product.discount}% OFF
          </Badge>
        )}
      </Box>

      <Box p="6">
        <Box display="flex" alignItems="baseline" mb={2}>
          <Badge borderRadius="full" px="2" colorScheme="blue">
            {product.category}
          </Badge>
          {product.stock <= 5 && (
            <Badge borderRadius="full" px="2" colorScheme="orange" ml={2}>
              ¡Últimas unidades!
            </Badge>
          )}
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

        <Text fontSize="sm" color="gray.600" noOfLines={2} mb={2}>
          {product.description}
        </Text>

        <Flex align="center" mb={2}>
          <Flex align="center">
            {[...Array(5)].map((_, i) => (
              <Icon
                key={i}
                as={FaStar}
                color={i < Math.floor(product.rating) ? "yellow.400" : "gray.300"}
                w={3}
                h={3}
              />
            ))}
          </Flex>
          <Text ml={1} fontSize="sm" color="gray.600">
            ({product.rating})
          </Text>
        </Flex>

        <Flex justify="space-between" align="center" mb={4}>
          <Stack spacing={0}>
            <Text fontSize="2xl" fontWeight="bold" color={textColor}>
              ${product.price.toFixed(2)}
            </Text>
            {product.discount > 0 && (
              <Text
                fontSize="sm"
                color="gray.500"
                textDecoration="line-through"
              >
                ${(product.price * (1 + product.discount/100)).toFixed(2)}
              </Text>
            )}
          </Stack>
          <Tooltip label={`${product.stock} unidades disponibles`}>
            <Flex align="center">
              <Icon as={BsBoxSeam} color="gray.500" />
              <Text ml={1} fontSize="sm" color="gray.500">
                {product.stock}
              </Text>
            </Flex>
          </Tooltip>
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
            onClick={() => onAddToCart(product)}
            flex={1}
            ml={2}
          >
            Agregar
          </Button>
        </Flex>
      </Box>
    </Box>
  );
};

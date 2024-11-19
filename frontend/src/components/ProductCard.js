import {
  Box,
  Image,
  Badge,
  Text,
  Button,
  Flex,
  Stack,
  useColorModeValue,
  Tooltip,
  IconButton
} from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import { FaShoppingCart, FaHeart, FaStar } from 'react-icons/fa';

const ProductCard = ({ product }) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.700', 'white');

  // Mapeo de categorías a imágenes
  const categoryImages = {
    'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    'Accessories': 'https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    'default': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
  };

  // Vulnerable: Renderiza HTML sin sanitizar (mantenemos la vulnerabilidad intencionalmente)
  const createMarkup = (html) => ({ __html: html });

  return (
    <Box
      maxW="sm"
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      bg={bgColor}
      _hover={{
        shadow: '2xl',
        transform: 'translateY(-4px)',
        transition: 'all 0.3s ease-in-out'
      }}
      position="relative"
    >
      {/* Badge de Oferta */}
      <Badge
        position="absolute"
        top="4"
        right="4"
        px="2"
        py="1"
        colorScheme="red"
        borderRadius="md"
        zIndex="1"
      >
        ¡Oferta!
      </Badge>

      <Box position="relative" overflow="hidden">
        <Image
          src={categoryImages[product.category] || categoryImages.default}
          alt={product.name}
          height="250px"
          width="100%"
          objectFit="cover"
          transition="transform 0.3s ease-in-out"
          _hover={{ transform: 'scale(1.05)' }}
        />

        {/* Overlay con acciones rápidas */}
        <Flex
          position="absolute"
          top="0"
          left="0"
          right="0"
          bottom="0"
          bg="blackAlpha.600"
          opacity="0"
          transition="opacity 0.3s"
          _groupHover={{ opacity: 1 }}
          justify="center"
          align="center"
        >
          <IconButton
            aria-label="Agregar a favoritos"
            icon={<FaHeart />}
            colorScheme="red"
            variant="solid"
            size="md"
            m="1"
          />
        </Flex>
      </Box>

      <Box p="6">
        <Box display="flex" alignItems="baseline" mb={2}>
          <Badge borderRadius="full" px="2" colorScheme="blue">
            {product.category}
          </Badge>
          <Flex align="center" ml="2">
            <FaStar color="gold" />
            <Text ml="1" fontSize="sm" color="gray.600">
              4.5
            </Text>
          </Flex>
        </Box>

        <Flex justify="space-between" align="baseline" mb={2}>
          <Tooltip label={product.name} placement="top">
            <Text
              fontWeight="semibold"
              fontSize="xl"
              color={textColor}
              noOfLines={2}
              cursor="pointer"
            >
              {product.name}
            </Text>
          </Tooltip>
        </Flex>

        {/* Vulnerable: XSS a través de la descripción (mantenemos la vulnerabilidad intencionalmente) */}
        <Box
          fontSize="sm"
          color="gray.600"
          mb={4}
          noOfLines={2}
          dangerouslySetInnerHTML={createMarkup(product.description)}
        />

        <Flex justify="space-between" align="center" mb={4}>
          <Stack spacing={0}>
            <Text fontSize="2xl" fontWeight="bold" color={textColor}>
              ${product.price?.toFixed(2)}
            </Text>
            <Text fontSize="sm" color="gray.500" textDecoration="line-through">
              ${(product.price * 1.2).toFixed(2)}
            </Text>
          </Stack>
        </Flex>

        <Flex justify="space-between" align="center">
          <Link to={`/product/${product.id}`} style={{ flex: 1, marginRight: 2 }}>
            <Button
              variant="outline"
              colorScheme="blue"
              width="100%"
              _hover={{
                bg: 'blue.50'
              }}
            >
              Ver detalles
            </Button>
          </Link>
          <Button
            colorScheme="blue"
            leftIcon={<FaShoppingCart />}
            flex={1}
            ml={2}
            _hover={{
              transform: 'scale(1.05)',
              transition: 'transform 0.2s'
            }}
          >
            Agregar
          </Button>
        </Flex>
      </Box>
    </Box>
  );
};

export default ProductCard;

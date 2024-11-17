import React, { useState } from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Box,
  Text,
  Image,
  Button,
  Select,
  useToast
} from '@chakra-ui/react';

// Mock de productos para comparar
const mockProducts = [
  {
    id: 1,
    name: "Laptop Gaming Pro",
    price: 1299.99,
    image: "https://source.unsplash.com/random/150x150?laptop",
    specs: {
      processor: "Intel i9",
      ram: "32GB",
      storage: "1TB SSD",
      graphics: "RTX 3080"
    }
  },
  {
    id: 2,
    name: "Laptop Business",
    price: 999.99,
    image: "https://source.unsplash.com/random/150x150?computer",
    specs: {
      processor: "Intel i7",
      ram: "16GB",
      storage: "512GB SSD",
      graphics: "Intel Iris"
    }
  },
  {
    id: 3,
    name: "Laptop Basic",
    price: 599.99,
    image: "https://source.unsplash.com/random/150x150?notebook",
    specs: {
      processor: "Intel i5",
      ram: "8GB",
      storage: "256GB SSD",
      graphics: "Intel UHD"
    }
  }
];

export const ProductComparison = () => {
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [availableProducts] = useState(mockProducts);
  const toast = useToast();

  // Vulnerable: No validación de entrada
  const addToComparison = (productId) => {
    const product = availableProducts.find(p => p.id === parseInt(productId));
    if (product) {
      // Vulnerable: No límite en la cantidad de productos a comparar
      setSelectedProducts([...selectedProducts, product]);

      // Vulnerable: Inyección directa de HTML
      const comparisonDiv = document.getElementById('comparison-container');
      if (comparisonDiv) {
        comparisonDiv.innerHTML += `
          <div class="product-card">
            <img src="${product.image}" alt="${product.name}" />
            <h3>${product.name}</h3>
            <p>$${product.price}</p>
          </div>
        `;
      }
    }
  };

  // Vulnerable: No validación de datos antes de guardar
  const saveComparison = () => {
    // Vulnerable: Almacenamiento de datos sensibles sin encriptación
    localStorage.setItem('savedComparisons', JSON.stringify(selectedProducts));

    toast({
      title: "Comparación guardada",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Box p={4}>
      <Text fontSize="2xl" mb={4}>Comparación de Productos</Text>

      <Box mb={4}>
        <Select
          placeholder="Agregar producto para comparar"
          onChange={(e) => addToComparison(e.target.value)}
        >
          {availableProducts.map((product) => (
            <option key={product.id} value={product.id}>
              {product.name} - ${product.price}
            </option>
          ))}
        </Select>
      </Box>

      <div id="comparison-container"></div>

      {selectedProducts.length > 0 && (
        <>
          <Table variant="simple" mt={4}>
            <Thead>
              <Tr>
                <Th>Características</Th>
                {selectedProducts.map((product) => (
                  <Th key={product.id}>{product.name}</Th>
                ))}
              </Tr>
            </Thead>
            <Tbody>
              <Tr>
                <Td>Imagen</Td>
                {selectedProducts.map((product) => (
                  <Td key={product.id}>
                    <Image
                      src={product.image}
                      alt={product.name}
                      boxSize="100px"
                      objectFit="cover"
                    />
                  </Td>
                ))}
              </Tr>
              <Tr>
                <Td>Precio</Td>
                {selectedProducts.map((product) => (
                  <Td key={product.id}>${product.price}</Td>
                ))}
              </Tr>
              <Tr>
                <Td>Procesador</Td>
                {selectedProducts.map((product) => (
                  <Td key={product.id}>{product.specs.processor}</Td>
                ))}
              </Tr>
              <Tr>
                <Td>RAM</Td>
                {selectedProducts.map((product) => (
                  <Td key={product.id}>{product.specs.ram}</Td>
                ))}
              </Tr>
              <Tr>
                <Td>Almacenamiento</Td>
                {selectedProducts.map((product) => (
                  <Td key={product.id}>{product.specs.storage}</Td>
                ))}
              </Tr>
              <Tr>
                <Td>Gráficos</Td>
                {selectedProducts.map((product) => (
                  <Td key={product.id}>{product.specs.graphics}</Td>
                ))}
              </Tr>
            </Tbody>
          </Table>

          <Button
            colorScheme="blue"
            mt={4}
            onClick={saveComparison}
          >
            Guardar Comparación
          </Button>
        </>
      )}
    </Box>
  );
};

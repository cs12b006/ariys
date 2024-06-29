import React from 'react';
import { StyleSheet, Text, FlatList, ActivityIndicator, View, Image } from 'react-native';
import { ListItem, SearchBar } from "react-native-elements";
import { ApolloClient, InMemoryCache, ApolloProvider, useQuery, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://192.168.86.216:8000/graphql/',
  cache: new InMemoryCache(),
});

const GET_PRODUCTS = gql`
  query MyQuery {
    products {
      id
      name
    }
  }
`;


const ProductsList = () => {
  const { loading, error, data } = useQuery(GET_PRODUCTS);
  console.log(data)

  if (loading) return <ActivityIndicator size="large" color="#0000ff" />;
  if (error) return <Text>Error: {error.message}</Text>;

  return (
  <FlatList
    data={data.products}
    renderItem={({ item }) => (
      <ListItem
        title={`${item.name}`}
        containerStyle={{ borderBottomWidth: 0, marginBottom: 20 }}
      />
    )}
    keyExtractor={item => item.id}
    ItemSeparatorComponent={() => <View style={{ height: 1, width: "86%", backgroundColor: "#CED0CE", marginLeft: "14%", marginTop: "3%" }} />}
    ListHeaderComponent={() => <SearchBar placeholder="Type Here..." lightTheme round />}
  />
  );
};

// Main component with ApolloProvider wrapping
const HomeScreen = () => {
  return (
    <ApolloProvider client={client}>
      <ProductsList />
    </ApolloProvider>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
   subtitleView: {
    flexDirection: 'column',
    paddingLeft: 10,
    paddingTop: 5,
    marginLeft: 110
  },
  menuText: {
    paddingLeft: 10,
    color: 'grey'
  },
  locText: {
    paddingLeft: 10,
    color: 'grey',
    marginTop: 6,
    fontSize: 12
  },
  titleText: {
    fontWeight: 'bold'
  },
  restaurantImage: {
    width: 600,
    height: 800
  }
});
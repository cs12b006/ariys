import React from 'react';
import { StyleSheet, Text, FlatList, ActivityIndicator, View, Image } from 'react-native';
import { Button, Card, ListItem, SearchBar } from "@rneui/themed";
import { ApolloClient, InMemoryCache, ApolloProvider, useQuery, gql } from '@apollo/client';
import { useFetchAllProductsQuery } from '../graphql/generated/types';

const client = new ApolloClient({
  uri: 'http://192.168.86.216:8000/graphql/',
  cache: new InMemoryCache(),
});


const ProductsList: React.FC = () => {
  const { loading, error, data } = useFetchAllProductsQuery();

  if (loading) return <ActivityIndicator size="large" color="#0000ff" />;
  if (error) return <Text>Error: {error.message}</Text>;
console.log(data);
  return (
    <FlatList
      data={data?.products ?? []}
      renderItem={({ item }) => (
        <Button
          title={item?.name}
          containerStyle={{ borderBottomWidth: 0, marginBottom: 20 }}
        />
      )}
      keyExtractor={item => item?.id ?? ''}
      ItemSeparatorComponent={() => <View style={{ height: 1, width: "86%", backgroundColor: "#CED0CE", marginLeft: "14%", marginTop: "3%" }} />}
      ListHeaderComponent={() => <SearchBar placeholder="Type Here..." lightTheme round />}
    />
  );
};

const HomeScreen: React.FC = () => {
  return (
    <ApolloProvider client={client}>
      <ProductsList />
    </ApolloProvider>
  );
};

export default HomeScreen;

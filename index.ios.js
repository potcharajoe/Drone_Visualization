/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View
} from 'react-native';

import MapView from 'react-native-maps';

export default class Drone_visualization extends Component {
  render() {
    return (
      
       <MapView style = {styles.container}
       followsUserLocation = {true}
       showsUserLocation = {true}
    initialRegion={{
      latitude: 37.78825,
      longitude: -100.4324,
      latitudeDelta: 0.0922,
      longitudeDelta: 0.0421,
    }} />
    
    );
  }
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  map: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
});

AppRegistry.registerComponent('Drone_visualization', () => Drone_visualization);

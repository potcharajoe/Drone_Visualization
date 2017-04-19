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
  View,
  Button
} from 'react-native';

import MapView from 'react-native-maps';
import axios from 'axios';

export default class Drone_visualization extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showText: true,
      annotate: 'My Locaition :D',
      region: {
        latitude: 13.8463,
        longitude: 100.5685,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      },
      markers:[
      {
        latlng:{
          latitude:13.9,
          longitude:100.8
        },
        title:'Station',      
        description:'position of station',
      }
      ]
    };
  }

  componentWillMount() {
      axios.get('http://localhost:9090/api/')
        .then(response => this.setState({

        }));
    }

  onRegionChange(region) {
    console.log(region)
    this.setState({
      region,
    });
  }

  onPress(cor,pos) {
    console.log(cor,pos)
    this.setState({
      cor,pos,
    });
  }


  render() {
    console.log(this.state.markers[0])
    return (
      <View style={{flex:1}}>
      <MapView style={{flex:1}}
        region={this.state.region}
        showsUserLocation = {true}
        showsMyLocationButton = {true}
        loadingEnabled = {true}
        onRegionChange={ (x)=>this.onRegionChange(x)}
        onPress = { (a)=>console.log(a) }
      >
        {this.state.markers.map(marker => (
        <MapView.Marker
            coordinate={marker.latlng}
            title={marker.title}
            description={marker.description}
            />
          ))}  
        </MapView>
        </View>
    );
  }

//   render() {
//     return (
//     <View style={{flex:1}}>

//        <MapView style = {{flex:1,margin:10}}
//         userLocationAnnotationTitle = {this.state.annotate}
//         region={
//           this.state.region
//         }
//         onRegionChange = { (x)=> this.changeLocation(x) }/>
//      <View style={{flex:1}}>
      
//      </View>
// </View>
//     );
//   }
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

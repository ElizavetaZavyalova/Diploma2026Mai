using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using YandexMaps;

[System.Serializable]
public class Marker
{
    public float lat;
    public float lon;
}

[System.Serializable]
public class MarkerResponse
{
    public List<Marker> markers;
}

public class MapSettings : MonoBehaviour
{
    public RawImage image;
    public Slider slider;

    public Map.TypeMap typeMap;
    public Map.TypeMapLayer mapLayer;
    public TMP_InputField device1;
    public TMP_InputField device2;
    public TextMeshProUGUI pos;


    public List<Vector2> markers = new List<Vector2>();

    private string url = "http://localhost:8083/points";
    private string urlEnd = null;

    void Start()
    {
        InvokeRepeating(nameof(UpdateMap), 0f, 1f);
    }
    
    public void resetPos()
    {
        urlEnd = "/" + device1.text + "/" + device2.text;
    }

    public bool needUpdate = true;

    public void stopUpdate()
    {
        urlEnd = null;
        needUpdate = false;
        pos.text= "";
    }

    private bool isLoading = false;
    

    void UpdateMap()
    {
        if (needUpdate && urlEnd != null && !isLoading)
        {
            StartCoroutine(GetPoint());
        }
    }

    IEnumerator GetPoint()
    {
        isLoading = true;

        UnityWebRequest request = UnityWebRequest.Get(url + urlEnd);

        request.SetRequestHeader("accept", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string json = request.downloadHandler.text;

            MarkerResponse response =
                JsonUtility.FromJson<MarkerResponse>(json);

            if (response.markers != null &&
                response.markers.Count > 0)
            {
                Marker endPoint =
                    response.markers[response.markers.Count - 1];

                markers.Clear();

                markers.Add(new Vector2(endPoint.lat, endPoint.lon));

                pos.text = $"{endPoint.lat:F3} : {endPoint.lon:F3}";

                LoadMap(endPoint.lat, endPoint.lon);
            }
        }
        else
        {
            Debug.LogError(request.error);
        }

        isLoading = false;
    }

    void LoadMap(float lat, float lon)
    {
        Map.EnabledLayer = true;

        Map.Size = Mathf.Clamp((int)slider.value, 0, 1000);

        Map.SetTypeMap = typeMap;
        Map.SetTypeMapLayer = mapLayer;

        Map.SetMarker = markers;

        Map.Latitude = markers[0].y;
        Map.Longitude =  markers[0].x;

        Map.LoadMap();

        StartCoroutine(LoadTexture());
    }

    IEnumerator LoadTexture()
    {
        yield return new WaitForSeconds(2f);

        image.texture = Map.GetTexture;
    }
}
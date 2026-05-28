using TMPro;
using UnityEngine;

public class SetNewPosition : MonoBehaviour
{
    private string SET_RADAR = "радар";
    private string SET_GEO = "геолокатор";
    public TMP_InputField device2;
    public TextMeshProUGUI name;
    private bool isGeo;
    public MapSettings settings;

    public void LoadInfo()
    {
        if (isGeo)
        {
            device2.gameObject.SetActive(false);
            name.text = SET_RADAR;
            settings.stopUpdate();
        }
        else
        {
            device2.gameObject.SetActive(true);
            name.text = SET_GEO;
        }

        isGeo = !isGeo;

    }
  
}

from enum import StrEnum, auto
from typing import TypedDict, NotRequired, Never, Literal
from mitmproxy import http


class Badge(StrEnum):
    boogie_basic = "boogie-basic"
    boogie_plus = "boogie-plus"
    boogie_tester = "boogie-tester"
    boogie_booster = "boogie-booster"
    boogie_founder = "boogie-founder"
    boogie_topg = "boogie-topg"
    epicgames = auto()


class defaultUserSettings(TypedDict):
    status: str
    useStatus: bool
    displayName: str
    configDisplayName: str
    launcherToken: str
    pipe: int
    lockerId: str
    deploymentId: str
    updatedTime: str
    creationTime: str
    athenaItemId: str
    premium: bool
    member: bool
    banned: bool
    accountId: str
    translations: "TranslationsFile | None"
    badges: list[Badge]
    replaceText: bool
    language: str
    accountId: str
    jid: str
    discordAccountId: str
    xmppFlow: http.HTTPFlow | None
    debug: bool
    savedUrl: str | None


class CommandoMessage(TypedDict):
    response: Literal["ok!"]
    command: Never


class profileForm(TypedDict):
    lang: str

    radio_enabled: bool
    nigga_enabled: bool
    video: str
    images_enabled: bool
    image: str
    replacements_enabled: bool
    status: str
    playlist: str
    display_name: str
    vbucks: int
    crowns: int
    battlestars: int
    levels: int


class ActiveLoadoutSlot(TypedDict):
    equippedItemId: NotRequired[str]
    itemCustomizations: list[Never]
    slotTemplate: str


class seasonInfo(TypedDict):
    seasonNumber: int
    numWins: int
    seasonXp: int
    seasonLevel: int
    bookXp: int
    bookLevel: int
    purchasedVIP: bool


class ActiveLoadoutLoadout(TypedDict):
    loadoutSlots: NotRequired[list[ActiveLoadoutSlot]]
    shuffleType: Literal["DISABLED"]


class ActiveLoadout(TypedDict):
    accountId: NotRequired[str]
    athenaItemId: str
    creationTime: str
    deploymentId: NotRequired[str]
    loadouts: dict[str, ActiveLoadoutLoadout]
    updatedTime: NotRequired[str]
    equippedPresetItemId: NotRequired[str]
    shuffleType: NotRequired[Literal["DISABLED"]]


class PresetResponseLoadouts(TypedDict):
    deploymentId: str
    accountId: str
    loadoutType: str
    displayName: str
    presetIndex: int
    athenaItemId: str
    creationTime: str
    updatedTime: str
    presetFavoriteStatus: Literal["EMPTY"]
    presetId: str


class LockerV3Items(TypedDict):
    activeLoadoutGroup: ActiveLoadout
    loadoutGroupPresets: list[PresetResponseLoadouts]
    loadoutPresets: list[Never]


class TranslationsFile(TypedDict):
    contritbutors: dict[str, str]
    aliases: dict[str, str]
    translations: dict[str, dict[str, str]]


class AthenaItemAttributesVariant(TypedDict):
    channel: str
    active: str
    owned: list[str]


class AthenaItemAttributesVictoryCrown(TypedDict):
    has_victory_crown: bool
    data_is_valid_for_mcp: bool
    total_victory_crowns_bestowed_count: int
    total_royal_royales_achieved_count: int


class AthenaLootList(TypedDict):
    itemProfile: str
    itemType: str
    itemGuid: str
    quantity: int


class commonCorePurchase(TypedDict):
    purchaseId: str
    offerId: str
    purchaseDate: str
    freeRefundEligible: bool
    fulfillments: list[dict[Never, Never]]
    lootResult: list[AthenaLootList]
    totalMtxPaid: int
    metadata: dict[Never, Never]
    gameContext: str


class AthenaItemAttributesParams(TypedDict):
    userMessage: str
    HeaderAssetString: str


class AthenaItemAttributes(TypedDict):
    display_name: NotRequired[str]
    slots: NotRequired[list["ConfigSavedPresetSlot"]]
    item_seen: NotRequired[bool]
    creation_time: NotRequired[None]
    favorite: NotRequired[bool]
    archived: NotRequired[bool]
    lootList: NotRequired[list[AthenaLootList]]
    fromAccountId: NotRequired[str]
    giftedOn: NotRequired[str]
    giftFromAccountId: NotRequired[str]
    variants: NotRequired[list[AthenaItemAttributesVariant]]
    victory_crown_account_data: NotRequired[AthenaItemAttributesVictoryCrown]
    max_level_bonus: NotRequired[int]
    level: NotRequired[int]
    xp: NotRequired[int]
    platform: NotRequired[str]
    params: NotRequired[AthenaItemAttributesParams]


class AthenaItem(TypedDict):
    attributes: AthenaItemAttributes
    quantity: int
    templateId: str


class LauncherInstalledInstallation(TypedDict):
    InstallLocation: str
    NamespaceId: str
    ItemId: str
    ArtifactId: str
    AppVersion: str
    AppName: str


class LauncherInstalled(TypedDict):
    InstallationList: list[LauncherInstalledInstallation]


class GameInfo(TypedDict):
    path: str
    version: str
    name: str
    id: str


class ConfigInviteExploit(TypedDict):
    enabled: NotRequired[bool]
    users: list[str]


class ConfigSavedPresetSlot(TypedDict):
    slot_template: str
    equipped_item: str


class ConfigSavedPreset(TypedDict):
    presetType: str
    presetId: int
    slots: list[ConfigSavedPresetSlot]


class ConfigSavedPresets(TypedDict):
    character: dict[str, ConfigSavedPreset]
    emotes: dict[str, ConfigSavedPreset]
    lobby: dict[str, ConfigSavedPreset]
    wraps: dict[str, ConfigSavedPreset]
    sports: dict[str, ConfigSavedPreset]
    suv: dict[str, ConfigSavedPreset]
    instruments: dict[str, ConfigSavedPreset]
    jam: dict[str, ConfigSavedPreset]


class ConfigSaved(TypedDict):
    presets: dict[str, PresetResponseLoadouts]
    favorite: list[str]
    archived: list[str]


class Config(TypedDict):
    configVersion: float
    tosAgreed: bool
    EveryCosmetic: NotRequired[bool]
    closeFortnite: bool
    Playlist: NotRequired[str]
    WebSocketLogging: bool
    updateSkip: bool
    refreshToken: NotRequired[str]
    InviteExploit: ConfigInviteExploit
    saved: ConfigSaved
    extraSettings: profileForm


class LightswitchServiceLauncherInfoDTO(TypedDict):
    appName: str
    catalogItemId: str
    namespace: str


class LightswitchService(TypedDict):
    serviceInstanceId: str
    status: str
    message: str
    maintenanceUri: None
    overrideCatalogIds: list[str]
    allowedActions: list[str]
    banned: bool
    launcherInfoDTO: LightswitchServiceLauncherInfoDTO


class CloudstorageSystemConfigTransport(TypedDict):
    name: str
    type: str
    appName: str
    isEnabled: bool
    isRequired: bool
    isPrimary: bool
    timeoutSeconds: int
    priority: int


class CloudstorageSystemConfigTransports(TypedDict):
    McpProxyTransport: CloudstorageSystemConfigTransport
    McpSignatoryTransport: CloudstorageSystemConfigTransport
    DssDirectTransport: CloudstorageSystemConfigTransport


class CloudstorageSystemConfig(TypedDict):
    lastUpdated: str
    disableV2: bool
    isAuthenticated: bool
    enumerateFilesPath: str
    enableMigration: bool
    enableWrites: bool
    epicAppName: str
    transports: CloudstorageSystemConfigTransports


LoadoutPresets = TypedDict(
    "LoadoutPresets",
    {
        "CosmeticLoadout:LoadoutSchema_Character": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Emotes": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Platform": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Wraps": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Jam": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Sparks": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Vehicle": dict[int, str],
        "CosmeticLoadout:LoadoutSchema_Vehicle_SUV": dict[int, str],
    },
)


class AthenaResponseProfileChangeProfileStats(TypedDict):
    loadout_presets: LoadoutPresets


class AthenaResponseProfileChangeProfile(TypedDict):
    created: str
    updated: str
    rvn: int
    wipeNumber: int
    accountId: str
    profileId: str
    version: str
    items: dict[str, AthenaItem]
    stats: NotRequired[AthenaResponseProfileChangeProfileStats]
    commandRevision: int
    profileCommandRevision: int
    profileChangesBaseRevision: int


class AthenaResponseProfileChange(TypedDict):
    changeType: str
    profile: AthenaResponseProfileChangeProfile


class AthenaResponse(TypedDict):
    profileRevision: int
    profileId: str
    profileChangesBaseRevision: int
    profileCommandRevision: int
    profileChanges: list[AthenaResponseProfileChange]

class XMPPMessage(TypedDict):
    sent: str
    type: str
    payload: str


class PresetResponse(TypedDict):
    accountId: str
    athenaItemId: str
    creationTime: str
    deploymentId: str
    displayName: str
    loadouts: PresetResponseLoadouts
    presetFavoriteStatus: Literal["EMPTY"]
    presetId: str
    presetIndex: int
    updatedTime: str


class ProfileInfo(TypedDict):
    member: bool
    premium: bool
    betaTester: bool
    banned: bool
    badges: list[Badge]


class RememberMe(TypedDict):
    Region: str
    Email: str
    Name: str
    LastName: str
    DisplayName: str
    Token: str
    bHasPasswordAuth: bool
    TokenUseCount: int


class commonCoreSurveyData(TypedDict):
    numTimesCompleted: int
    lastTimeCompleted: str


class commonCoreMtxPurchase(TypedDict):
    purchaseId: str
    offerId: str
    purchaseDate: str
    freeRefundEligible: bool
    fulfillments: list[dict[Never, Never]]
    lootResult: list[AthenaLootList]
    totalMtxPaid: int
    metadata: dict[Never, Never]
    gameContext: str


class commonCoreMtxPurchaseHistory(TypedDict):
    refundsUsed: int
    refundCredits: int
    tokenRefreshReferenceTime: str
    purchases: list[commonCoreMtxPurchase]


class commonCoreDatePurchases(TypedDict):
    lastInterval: str
    purchaseList: dict[str, int]


class commonCoreInAppPurchases(TypedDict):
    reciepts: list[None]
    fulfillmentCounts: dict[str, int]


class commonCoreRmtPurchaseHistory(TypedDict):
    fulfillmentId: str
    purchaseDate: str
    lootResult: list[AthenaLootList]


class commonCoreGiftHistory(TypedDict):
    sentTo: dict[str, str]
    receivedFrom: dict[str, str]
    num_sent: int
    num_received: int
    gifts: list[None]


class commonCoreStatAttributes(TypedDict):
    survey_data: dict[Literal["metadata"], NotRequired[dict[str, commonCoreSurveyData]]]
    item_sync: dict[str, str]
    intro_game_played: bool
    mtx_purchase_history: commonCoreMtxPurchaseHistory
    mtx_affiliate_set_time: str
    current_mtx_platform: Literal["EpicPC"]
    mtx_affiliate: str
    weekly_purchases: commonCoreDatePurchases
    daily_purchases: commonCoreDatePurchases
    in_app_purchases: commonCoreInAppPurchases
    forced_intro_played: NotRequired[str]
    rmt_purchase_history: commonCoreRmtPurchaseHistory
    undo_timeout: str
    monthly_purchases: commonCoreDatePurchases
    allowed_to_send_gifts: bool
    mfa_enabled: bool
    gift_history: commonCoreGiftHistory


class commonCoreStats(TypedDict):
    attributes: commonCoreStatAttributes


class fullProfileUpdateProfile(TypedDict):
    created: str
    updated: str
    rvn: int
    wipeNumber: int
    accountId: str
    profileId: Literal["common_core", "athena"]
    version: str
    items: dict[str, AthenaItemAttributes]
    stats: commonCoreStats
    commandRevision: int
    _id: str
    profileCommandRevision: int
    profileChangesBaseRevision: int


class fullProfileUpdate(TypedDict):
    changeType: Literal["fullProfileUpdate"]
    profile: fullProfileUpdateProfile
    profileCommandRevision: int
    serverTime: str
    responseVersion: Literal[1]


class commonCoreFullProfile(TypedDict):
    profileRevision: int
    profileId: Literal["common_core"]
    profileChangesBaseRevision: int
    profileChanges: tuple[fullProfileUpdate]
    profileCommandRevision: int
    serverTime: str
    responseVersion: Literal[1]


class PartyConfigData(TypedDict):
    discoverability: Literal["ALL"]
    joinability: Literal["OPEN"]


PartyUpdateData = TypedDict(
    "PartyUpdateData",
    {
        "urn:epic:cfg:accepting-members_b": str,
        "Default:PartyMatchmakingInfo_j": str,
        "Default:PrimaryGameSessionId_s": str,
        "Default:GameSessionKey_s": str,
        "Default:AllowJoinInProgress_b": str,
        "Default:SelectedIsland_j": str,
        "Default:PartyState_s": str,
        "Default:CreativeInGameReadyCheckStatus_s": str,
    },
)


class PartyMetaData(TypedDict):
    delete: list[str]
    update: PartyUpdateData


class PartyData(TypedDict):
    config: PartyConfigData
    meta: PartyMetaData
    revision: int


class WebsocketInitialMessageInfo(TypedDict):
    id: int


class WebsocketInitialMessage(TypedDict):
    request: Literal["connect"]
    info: WebsocketInitialMessageInfo

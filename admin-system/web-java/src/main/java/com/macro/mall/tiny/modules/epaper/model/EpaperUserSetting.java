package com.macro.mall.tiny.modules.epaper.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import java.util.Date;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

/**
 * <p>
 * 用户设置
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@Getter
@Setter
@TableName("epaper_user_setting")
@Schema(name = "EpaperUserSetting", description = "用户设置")
public class EpaperUserSetting implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(value = "epaper_uid", type = IdType.AUTO)
    private Integer epaperUid;

    @Schema(description = "wifi_ssid，不知道有没有用，先设计再说")
    private String wifiSsid;

    @Schema(description = "wifi密码")
    private String wifiPassword;

    private Long umsUserId;

    @Schema(description = "对应标号")
    private String urban;

    private Date updateTime;

    // 设置字段映射
    @Schema(description = "是否关闭")
    @TableField(value = "deletee")
    private Boolean deletee;

    @Schema(description = "心跳")
    @TableField(value = "heartbeat_time")
    private Date HeartBeatTime;

    @Schema(description = "ip")
    private String ip;
}

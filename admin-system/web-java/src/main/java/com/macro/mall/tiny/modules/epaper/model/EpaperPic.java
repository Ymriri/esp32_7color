package com.macro.mall.tiny.modules.epaper.model;

import com.baomidou.mybatisplus.annotation.*;

import java.io.Serializable;
import java.util.Date;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

/**
 * <p>
 * 电子日历管理
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@Getter
@Setter
@TableName("epaper_pic")
@Schema(name = "EpaperPic", description = "电子日历管理")
public class EpaperPic implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "标号")
    @TableId(value = "epaper_uid", type = IdType.AUTO)
    private Integer epaperUid;

    @Schema(description = "用户Id")
    private Long userId;

    private Integer epaperOriginalId;

    @Schema(description = "日期")
    private Date date;

    @TableField(updateStrategy = FieldStrategy.IGNORED)
    @Schema(description = "文件名称")
    private String file;

    @Schema(description = "更新时间")
    private Date updateTime;

    @TableField(exist = false)
    private EpaperOriginal epaperOriginal;

    @Schema(description = "魔法数字")
    @TableField(value = "magic")
    private String magic;


}

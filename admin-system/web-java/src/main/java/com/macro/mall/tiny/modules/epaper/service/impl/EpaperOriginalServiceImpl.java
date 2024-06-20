package com.macro.mall.tiny.modules.epaper.service.impl;

import cn.hutool.core.date.DateUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.macro.mall.tiny.modules.epaper.dto.EpaperPicBindUserDto;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperPicMapper;
import com.macro.mall.tiny.modules.epaper.model.EpaperOriginal;
import com.macro.mall.tiny.modules.epaper.mapper.EpaperOriginalMapper;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import com.macro.mall.tiny.modules.epaper.service.EpaperOriginalService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.macro.mall.tiny.modules.ums.mapper.UmsAdminRoleRelationMapper;
import com.macro.mall.tiny.modules.ums.model.UmsAdmin;
import com.macro.mall.tiny.modules.ums.model.UmsAdminRoleRelation;
import com.macro.mall.tiny.modules.ums.service.impl.UmsAdminServiceImpl;
import com.macro.mall.tiny.security.util.JwtTokenUtil;
import com.macro.mall.tiny.security.util.YmriUtils;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * <p>
 * 服务实现类
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@Service
public class EpaperOriginalServiceImpl extends ServiceImpl<EpaperOriginalMapper, EpaperOriginal> implements EpaperOriginalService {

    @Autowired
    private EpaperOriginalMapper epaperOriginalMapper;

    @Autowired
    private YmriUtils ymriUtils;

    @Resource
    private JwtTokenUtil jwtTokenUtil;

    @Resource
    private UmsAdminServiceImpl umsAdminService;

    @Resource
    private UmsAdminRoleRelationMapper umsAdminRoleRelationMapper;

    @Resource
    private EpaperPicMapper epaperPicMapper;


    private static final Logger LOGGER = LoggerFactory.getLogger(EpaperOriginalServiceImpl.class);

    /**
     * 根据title和描述搜索
     *
     * @param keyword
     * @param pageSize
     * @param pageNum
     * @return
     */
    @Override
    public Page<EpaperOriginal> list(String keyword, Integer pageSize, Integer pageNum) {
        Page<EpaperOriginal> page = new Page<>(pageNum, pageSize);
        QueryWrapper<EpaperOriginal> wrapper = new QueryWrapper<>();
        LambdaQueryWrapper<EpaperOriginal> lambda = wrapper.lambda();
        if (StrUtil.isNotEmpty(keyword)) {
            // 根据标题搜索
            lambda.like(EpaperOriginal::getTitle, keyword);
            lambda.or().like(EpaperOriginal::getDescription, keyword);
        }
        return page(page, wrapper);
    }

    @Override
    public EpaperOriginal create(EpaperOriginal epaperOriginal) {
        try {
            epaperOriginal.setFileId(null);
            epaperOriginal.setUpdateTime(new Date());
            boolean success = this.save(epaperOriginal);
            if (success) return epaperOriginal;
            else return null;
        } catch (Exception e) {
            LOGGER.error("素材插入失败");
            return null;
        }
    }

    @Override
    public boolean delete(Integer id) {
        try {
            epaperOriginalMapper.deleteById(id);
            return true;
        } catch (Exception e) {
            throw new RuntimeException(e);

        }

    }

    @Override
    public boolean showPic(Integer id, HttpServletResponse response) {
        // 任意用户都可以查看
        try {
            EpaperOriginal epaperOriginal = epaperOriginalMapper.selectById(id);
            if (epaperOriginal == null) {
                return false;
            }
            // 特殊处理
            String filePath = epaperOriginal.getPicPath().replace(" ", "");
            return ymriUtils.showPic(filePath, response);
        } catch (IOException e) {
            return false;
        }
    }

    public String createOutPic(Integer id, String execString) {
        try {
            EpaperOriginal epaperOriginal = epaperOriginalMapper.selectById(id);
            if (epaperOriginal == null) {
                return null;
            }
            String filePath = ymriUtils.fileHead + epaperOriginal.getPicPath().replace(" ", "");
            // 调用python生成图片，前面不变，后面加参数
            execString = "python3 " + ymriUtils.pythonPath + " --imgPath=" + filePath + " " + execString;
            Process proc = null;
            BufferedReader in = null;
            try {
                LOGGER.info(execString);
                // 执行py文件
                proc = Runtime.getRuntime().exec(execString);
                //用输入输出流来截取结果
                in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
                var ret = proc.waitFor();
                String line = null;
                while ((line = in.readLine()) != null) {
                    filePath = line;
                }
                return filePath;
                // 关闭所有流
            } catch (IOException | InterruptedException e) {
                LOGGER.warn(e.getMessage());
                return null;
            } finally {
                if (proc != null) {
                    proc.destroy();
                }
                if (in != null) {
                    in.close();
                }
            }
        } catch (IOException e) {
            return null;
        }
    }

    public Boolean coverPic(String picPath, String outName) {

        String execString =  ymriUtils.coverPath + " "+picPath + " " + outName;
        Process proc = null;
        BufferedReader in = null;
        try {
            LOGGER.info(execString);
            // 执行py文件
            proc = Runtime.getRuntime().exec(execString);
            //用输入输出流来截取结果
            var ret = proc.waitFor();
            // 执行返回获得结果
            return ret == 0;
        } catch (IOException | InterruptedException e) {
            LOGGER.warn(e.getMessage());
            LOGGER.warn("图片转换异常....");
            return false;
        } finally {
            if (proc != null) {
                proc.destroy();
            }

        }

    }

    /**
     * 生成预览图
     * PS: 该方法存在并发问题，但是由于用户有限所以暂不优化
     *
     * @param id       id
     * @param response response
     * @return boolean
     */
    public void showOutPic(Integer id, HttpServletResponse response) {
        // 任意用户都可以查看
        try {
            String exeString = "--out=" + ymriUtils.tempPath + " --outName=test.png";
            String filePath = this.createOutPic(id, exeString);
            if (filePath == null) {
                return;
            }
            ymriUtils.showAbsPic(filePath, response);
        } catch (IOException e) {
            return;
        }
    }

    /**
     * 显示用户图片
     *
     * @param fileName
     * @param response
     */
    public void showUserPic(String fileName, HttpServletResponse response) {
        try {
            // 替换路径
            fileName = "/" + fileName.replace("_", "/");
            // 请求发过来的时候自己加前缀
            ymriUtils.showAbsPic(ymriUtils.calendarPath + fileName, response);
        } catch (IOException e) {
            return;
        }
    }

    /**
     * 替换特定那天的图片
     *
     * @param epaperPicBindUserDto 绑定dto
     * @return boolean
     */
    public boolean createPicBindUser(EpaperPicBindUserDto epaperPicBindUserDto) {

        String userName = jwtTokenUtil.getUserName();
        // 检查用户是否有权限给别人设置，只有管理员才能给别人设置（9）
        UmsAdmin user = umsAdminService.getAdminByUsername(userName);
        UmsAdminRoleRelation umsAdminRoleRelation = umsAdminRoleRelationMapper.selectOne(new QueryWrapper<UmsAdminRoleRelation>().lambda().eq(UmsAdminRoleRelation::getAdminId, user.getId()).eq(UmsAdminRoleRelation::getRoleId, 10));
        if (umsAdminRoleRelation == null && epaperPicBindUserDto.getUserId() != user.getId()) {
            return false;
        }
        user = null;
        if (epaperPicBindUserDto.getUserId() != 0) {
            // 管理员才有的特判
            user = umsAdminService.getById(epaperPicBindUserDto.getUserId());
            if (user == null) {
                return false;
            }
        }

        Date date = epaperPicBindUserDto.getBindTime();
        String day = DateUtil.formatDate(date).replace("-", "");
        String fileName = day + ".png";
        String exeString = "--out=" + ymriUtils.calendarPath + " --outName=" + fileName + " --day=" + day;
        if (user != null) {
            exeString += " --user=" + user.getId();
        }
        // 保证天气一致性，这里并不直接生成，只是打个标签
//        String filePath = this.createOutPic(epaperPicBindUserDto.getPicId(), exeString);
//        if (filePath == null) {
//            return false;
//        }
        boolean flag = false;
        // 检查那天是否插入过
        EpaperPic epaperPic = epaperPicMapper.selectOne(new QueryWrapper<EpaperPic>().lambda().eq(EpaperPic::getUserId, epaperPicBindUserDto.getUserId()).eq(EpaperPic::getDate, date));
        if (epaperPic == null) {
            epaperPic = new EpaperPic();
            epaperPic.setUserId(epaperPicBindUserDto.getUserId());
            flag = true;
        }
        // 插入数据
        epaperPic.setEpaperOriginalId(epaperPicBindUserDto.getPicId());
        epaperPic.setDate(date);
        // 设置为空，覆盖以前已经生成过的
        epaperPic.setFile(null);
        epaperPic.setUpdateTime(new Date());
        int ret = 0;
        if (flag) {
            ret = epaperPicMapper.insert(epaperPic);
        } else {
            ret = epaperPicMapper.updateById(epaperPic);
        }
        return ret > 0;
    }

    @Override
    public boolean uploadPic(Integer id, MultipartFile img) {
        EpaperOriginal epaperOriginal = epaperOriginalMapper.selectById(id);
        if (epaperOriginal == null) {
            return false;
        }
        // 上传图片
        String fileName = img.getOriginalFilename();
        String stffixName = fileName.substring(fileName.lastIndexOf("."));
        // 重命名文件
        String picName = epaperOriginal.getTitle().replace(" ", "") + "___" + epaperOriginal.getDescription().replace(" ", "");
        String imgPath = ymriUtils.fileHead + picName + "." + stffixName;
        try {
            img.transferTo(new File(imgPath));
        } catch (Exception e) {
            LOGGER.error(e.getMessage());
            return false;
        }
        return true;
    }

    @Override
    public List<UmsAdmin> getPushUser() {
        String userName = jwtTokenUtil.getUserName();

        UmsAdmin user = umsAdminService.getAdminByUsername(userName);
        assert user != null;
        List<UmsAdmin> retList = new ArrayList<UmsAdmin>();
        // 根据user 关联查找是否具有权利role
        QueryWrapper<UmsAdminRoleRelation> wrapper = new QueryWrapper<>();
        // 先设定死为10吧，反正短期也不会修改
        LambdaQueryWrapper<UmsAdminRoleRelation> lambdaQueryWrapper = wrapper.lambda();
        lambdaQueryWrapper.eq(UmsAdminRoleRelation::getAdminId, user.getId()).and(i -> i.eq(UmsAdminRoleRelation::getRoleId, 10));
        UmsAdminRoleRelation temp = umsAdminRoleRelationMapper.selectOne(wrapper);
        if (temp != null) {
            wrapper.clear();
            wrapper.eq("role_id", 9);
            // 查询出所有的用户
            List<UmsAdminRoleRelation> umsAdminRoleRelations = umsAdminRoleRelationMapper.selectList(wrapper);
            for (UmsAdminRoleRelation umsAdminRoleRelation : umsAdminRoleRelations) {
                UmsAdmin tempUser = umsAdminService.getById(umsAdminRoleRelation.getAdminId());
                if (tempUser != null && tempUser.getStatus() != 0) {
                    retList.add(tempUser);
                }
            }
            // 添加给所有人推送的
            UmsAdmin vir = new UmsAdmin();
            vir.setId(0L);
            vir.setUsername("所有人");
            vir.setNickName("所有人");
            retList.add(vir);
        } else {
            retList.add(user);
        }
        return retList;
    }

}
